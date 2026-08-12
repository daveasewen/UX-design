#!/usr/bin/env python3
"""
_build_states_probe.py — ADVISORY states-completeness probe (NON-GATING).

Reports, per component, whether its gated reference snippet demonstrates the four
data/async UX states that matter for handoff completeness:

    empty · loading · error · overflow

This is a *map of what's shown vs. what's relevant*, not a standard. It does NOT
gate the build and NEVER exits non-zero (tiering is strategy-owned — see
_BUILD-CHAT-HANDOFF.md). Two layers:

  1. APPLICABILITY — a curated per-component judgement of which states are even
     relevant (a Divider has no "loading" state; a Table has all four). These are
     heuristic calls for Dave to sanity-check, surfaced explicitly in the report —
     NOT canon. Edit STATE_APPLICABILITY to correct them.
  2. EVIDENCE — keyword/markup scan of the snippet HTML + its embedded comment and
     the component meta, to detect whether an applicable state appears to be shown.

Output: tokens/_manifests/states-probe.json (machine) + _STATES-COMPLETENESS.md (human).
Regenerated each build so it never goes stale. Pure derivation — no visual decisions.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

STATES = ["empty", "loading", "error", "overflow"]

# --- Layer 1: curated applicability (heuristic — for Dave to confirm) -----------
# True  = this state is relevant for the component and we'd expect the canon to show it
# False = not meaningfully applicable (so absence is not a gap)
# Keyed by the snippet manifest `component` name.
STATE_APPLICABILITY = {
    "Accordion":          {"empty": False, "loading": False, "error": False, "overflow": True},
    "Avatar":             {"empty": True,  "loading": False, "error": True,  "overflow": False},
    "Badge":              {"empty": False, "loading": False, "error": False, "overflow": True},
    "Breadcrumbs":        {"empty": False, "loading": False, "error": False, "overflow": True},
    "Button":             {"empty": False, "loading": True,  "error": False, "overflow": False},
    "Cards":              {"empty": True,  "loading": True,  "error": True,  "overflow": True},
    "Countdown timer":    {"empty": False, "loading": False, "error": False, "overflow": False},
    "Divider":            {"empty": False, "loading": False, "error": False, "overflow": False},
    "Dropdown":           {"empty": True,  "loading": True,  "error": True,  "overflow": True},
    "Headers":            {"empty": False, "loading": False, "error": False, "overflow": True},
    "Hero":               {"empty": False, "loading": False, "error": False, "overflow": True},
    "Input fields":       {"empty": True,  "loading": False, "error": True,  "overflow": True},
    "Links":              {"empty": False, "loading": False, "error": False, "overflow": True},
    "List items":         {"empty": True,  "loading": True,  "error": False, "overflow": True},
    "Loading indicator":  {"empty": False, "loading": True,  "error": False, "overflow": False},
    "Modals":             {"empty": False, "loading": True,  "error": True,  "overflow": True},
    "Navigations":        {"empty": False, "loading": False, "error": False, "overflow": True},
    "Notifications":      {"empty": False, "loading": False, "error": True,  "overflow": True},
    "Pagination":         {"empty": True,  "loading": False, "error": False, "overflow": True},
    "Progress tracker":   {"empty": False, "loading": False, "error": True,  "overflow": True},
    "Quick actions":      {"empty": True,  "loading": False, "error": False, "overflow": True},
    "Reorder":            {"empty": False, "loading": False, "error": False, "overflow": False},
    "Search field":       {"empty": True,  "loading": True,  "error": True,  "overflow": True},
    "Selection controls": {"empty": False, "loading": False, "error": True,  "overflow": False},
    "Slider":             {"empty": False, "loading": False, "error": False, "overflow": False},
    "Status indicator":   {"empty": False, "loading": False, "error": True,  "overflow": False},
    "Table":              {"empty": True,  "loading": True,  "error": True,  "overflow": True},
    "Tabs":               {"empty": False, "loading": False, "error": False, "overflow": True},
    "Tags":               {"empty": False, "loading": False, "error": False, "overflow": True},
    "Tooltip":            {"empty": False, "loading": False, "error": False, "overflow": True},
    "Video player":       {"empty": False, "loading": True,  "error": True,  "overflow": False},
    "View options":       {"empty": False, "loading": False, "error": False, "overflow": False},
}

# --- Layer 2: evidence keywords (word-boundary matched, case-insensitive) -------
STATE_KEYWORDS = {
    "empty":    [r"empty", r"no results", r"no data", r"no items", r"nothing (here|to show)",
                 r"zero[- ]state", r"placeholder", r"fallback", r"initials", r"\bblank\b"],
    "loading":  [r"loading", r"spinner", r"skeleton", r"shimmer", r"aria-busy", r"busy",
                 r"buffering", r"please wait", r"\bpending\b", r"in[- ]progress"],
    "error":    [r"\berror", r"invalid", r"\bfailed?\b", r"retry", r"aria-invalid",
                 r"validation", r"went wrong", r"rag/(danger|error|warning)", r"\bdanger\b",
                 r"required", r"\bwarn"],
    "overflow": [r"overflow", r"truncat", r"ellipsis", r"text-overflow", r"line-clamp",
                 r"-webkit-line-clamp", r"\bclamp\b", r"\bscroll", r"show more", r"\+\d+ more",
                 r"collaps", r"reflow", r"wrap"],
}
COMPILED = {s: [re.compile(p, re.I) for p in pats] for s, pats in STATE_KEYWORDS.items()}


def load_snippets():
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "snippets", "*.reference.html"))):
        text = open(f, encoding="utf-8").read()
        m = re.search(r'id="token-manifest"[^>]*>(.*?)</script>', text, re.S)
        comp = json.loads(m.group(1)).get("component") if m else None
        if not comp:
            # fall back to filename
            comp = os.path.basename(f).replace(".reference.html", "").replace("-", " ")
        out[comp] = (os.path.basename(f), text)
    return out


def load_meta_text():
    out = {}
    for f in glob.glob(os.path.join(HERE, "components", "*.meta.json")):
        b = os.path.basename(f)
        if b.startswith("EXAMPLE") or b.startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        name = d.get("name")
        if name:
            out[name] = json.dumps(d)  # whole meta as a text blob for keyword scan
    return out


def detect(text, state):
    hits = sorted({m.group(0).lower()
                   for pat in COMPILED[state]
                   for m in [pat.search(text)] if m})
    return hits


def main():
    snippets = load_snippets()
    metas = load_meta_text()

    rows = []
    for comp in sorted(STATE_APPLICABILITY):
        applic = STATE_APPLICABILITY[comp]
        snip = snippets.get(comp)
        blob = (snip[1] if snip else "") + " " + metas.get(comp, "")
        rec = {"component": comp,
               "snippet": snip[0] if snip else None,
               "states": {}}
        for s in STATES:
            relevant = applic[s]
            hits = detect(blob, s) if relevant else []
            rec["states"][s] = {
                "applicable": relevant,
                "demonstrated": bool(hits) if relevant else None,
                "evidence": hits if relevant else [],
            }
        rows.append(rec)

    # ---- machine output ----
    man_dir = os.path.join(HERE, "tokens", "_manifests")
    os.makedirs(man_dir, exist_ok=True)
    out_json = os.path.join(man_dir, "states-probe.json")
    json.dump({"$advisory": True, "$nonGating": True, "states": STATES, "components": rows},
              open(out_json, "w", encoding="utf-8"), indent=1)

    # ---- summary numbers ----
    applic_total = sum(1 for r in rows for s in STATES if r["states"][s]["applicable"])
    shown_total = sum(1 for r in rows for s in STATES
                      if r["states"][s]["applicable"] and r["states"][s]["demonstrated"])
    gaps = [(r["component"], s) for r in rows for s in STATES
            if r["states"][s]["applicable"] and not r["states"][s]["demonstrated"]]

    # ---- human report ----
    def cell(st):
        if not st["applicable"]:
            return "·"            # not applicable
        return "✓" if st["demonstrated"] else "✗"

    lines = []
    lines.append("# States-completeness probe — ADVISORY (non-gating)\n")
    lines.append("*Auto-generated by `_build_states_probe.py`, regenerated each build. "
                 "This is a map of which data/async UX states the canon demonstrates vs. which are "
                 "relevant — **not** a gate and **not** canon. Applicability calls are heuristic; "
                 "correct them in `STATE_APPLICABILITY` if any look wrong.*\n")
    lines.append(f"**Coverage:** {shown_total}/{applic_total} applicable states demonstrated "
                 f"in the canon · {len(gaps)} advisory gap(s).\n")
    lines.append("Legend: ✓ shown · ✗ applicable but not shown (advisory gap) · · not applicable\n")
    lines.append("| Component | empty | loading | error | overflow |")
    lines.append("|---|:--:|:--:|:--:|:--:|")
    for r in rows:
        s = r["states"]
        lines.append(f"| {r['component']} | {cell(s['empty'])} | {cell(s['loading'])} "
                     f"| {cell(s['error'])} | {cell(s['overflow'])} |")
    lines.append("")
    lines.append("## Advisory gaps (applicable state not evidenced in the snippet)\n")
    if gaps:
        by_comp = {}
        for c, s in gaps:
            by_comp.setdefault(c, []).append(s)
        for c in sorted(by_comp):
            lines.append(f"- **{c}** — {', '.join(by_comp[c])}")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("## Notes\n")
    lines.append("- Evidence is keyword/markup detection over the snippet HTML + its embedded "
                 "comment + the component meta. A ✓ means the state is *mentioned or shown*; it is "
                 "not a guarantee the visual treatment is complete — that's a lane-B visual check.")
    lines.append("- A ✗ is a prompt to look, not a defect. Some states are intentionally out of "
                 "scope for a token-canon snippet (e.g. live async loading).")
    lines.append("- Nothing here changes the build result; the probe always exits 0.")

    out_md = os.path.join(HERE, "_STATES-COMPLETENESS.md")
    open(out_md, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    print(f"states probe: {shown_total}/{applic_total} applicable states demonstrated, "
          f"{len(gaps)} advisory gap(s) — wrote _STATES-COMPLETENESS.md + states-probe.json (non-gating)")
    return 0


if __name__ == "__main__":
    import sys
    try:
        main()
    except Exception as e:
        # Advisory: never break the build.
        print(f"states probe: skipped due to error: {e} (non-gating)")
    sys.exit(0)
