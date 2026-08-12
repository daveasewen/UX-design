#!/usr/bin/env python3
"""
Knowledge-usage trace — retrieved-vs-invented, reconstructed from the artifact itself.

WHY (Dave, §9 session 2026-07-07): the §9 spread verdict was "confused, not converged" — the
open question is whether the engine's ceiling is a RULES problem (better prompt-crafting fixes it)
or an ARCHITECTURE problem (one governed pass caps out below a two-pass "generate free, then
constrain+verify" pipeline). To answer that empirically we need comparable data on what each
lineage (governed-Sonnet, governed-Opus, gravity-fix, diagnostic) actually RETRIEVED from the
knowledge base vs INVENTED free-hand.

The existing spread artifacts carry no self-report, so this tool RECONSTRUCTS the trace directly
from each HTML file — no manifest required retroactively. It extends two existing techniques:
  - _validate_icons.py's byte-match (inline SVG paths vs assets/icons/ library);
  - the token/component map (var() refs resolved against canon.css's defined vars + .cn-* set).

WHAT IT MEASURES per file (all brand-bearing surfaces the §9 cardinal curbs govern):
  - canon_linked      : is canon/canon.css actually linked + class="canon" on root? (retrieval on/off)
  - components        : distinct real .cn-* used (RETRIEVED composition) vs .cn-*-looking-but-unknown
  - hex_live          : raw #rrggbb literals in LIVE css (comments stripped) = INVENTED brand values.
                        Colour is a CARDINAL curb — it must be retrieved, never typed. Any live hex
                        is a cardinal violation, and the headline invention signal.
  - var_canon         : var(--x) whose name IS defined in canon.css        = RETRIEVED token
  - var_local         : var(--x) defined only in THIS file, not in canon    = INVENTED token/palette
  - var_dangling      : var(--x) defined nowhere                            = broken ref
  - icons             : inline paths — library byte-match vs UNKNOWN (reuses the icon gate technique)
  - candidates        : declared derive-and-flag markers (data-candidate / CANDIDATE / FLAG comments)

It then assigns a coarse RETRIEVAL POSTURE per file and aggregates per lineage, so the four
lineages can be compared on one axis: how much of what reads-as-brand was pulled from the KB vs
made up. That comparison is the empirical half of the rules-vs-architecture question.

NOT a gate; a measurement instrument. Source of truth stays the authored canon.

Usage:
  python3 _trace_knowledge_usage.py                       # default: trace the 07-05 §9 spread
  python3 _trace_knowledge_usage.py LABEL=path [LABEL=path ...]   # custom lineages (file or dir)
  python3 _trace_knowledge_usage.py --json                # also dump machine JSON
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "canon", "canon.css")
ICONS = os.path.join(HERE, "assets", "icons")
OUT_MD = os.path.join(HERE, "_KNOWLEDGE-USAGE-TRACE.md")
OUT_JSON = os.path.join(HERE, "_KNOWLEDGE-USAGE-TRACE.json")

# ---- regexes ----
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
VAR_REF = re.compile(r"var\(\s*(--[a-z0-9-]+)")
VAR_DEF = re.compile(r"(--[a-z0-9-]+)\s*:")
CN_CLASS = re.compile(r"\bcn-[a-z0-9-]+")
C_CLASS = re.compile(r"\bc-[a-z0-9-]+")
SVGRE = re.compile(r"<svg\b[^>]*?>.*?</svg>", re.S)
DRE = re.compile(r'\bd="([^"]+)"')
SHAPERE = re.compile(r"<(?:circle|rect|ellipse|polygon|polyline)\b")
CANDIDATE = re.compile(r"data-candidate|CANDIDATE|derive-and-flag|FLAG:|/\*\s*flag", re.I)


def norm(d):
    return re.sub(r"\s+", " ", d.strip())


def canon_vars():
    """Every --token defined in canon.css = the retrievable token vocabulary."""
    try:
        s = open(CANON, encoding="utf-8").read()
    except Exception:
        return set(), set()
    defined = set(VAR_DEF.findall(s))
    cn = set(CN_CLASS.findall(s))
    return defined, cn


def icon_library():
    lib = set()
    for f in glob.glob(os.path.join(ICONS, "**", "*.svg"), recursive=True):
        try:
            s = open(f, encoding="utf-8").read()
        except Exception:
            continue
        for d in DRE.findall(s):
            lib.add(norm(d))
    return lib


CANON_VARS, CANON_CN = canon_vars()
ICON_LIB = icon_library()


def strip_comments(html):
    return HTML_COMMENT.sub("", CSS_COMMENT.sub("", html))


def trace_file(path):
    raw = open(path, encoding="utf-8").read()
    live = strip_comments(raw)

    # local var definitions in this file (its own :root / rules)
    local_defs = set(VAR_DEF.findall(live))

    canon_linked = ("canon.css" in raw) and ('class="canon"' in raw or "class='canon'" in raw)

    # colour: live hex = invented cardinal value
    hex_live = HEX.findall(live)

    # var refs resolved against canon vs local-only vs dangling
    var_canon = var_local = var_dangling = 0
    for name in VAR_REF.findall(live):
        if name in CANON_VARS:
            var_canon += 1
        elif name in local_defs:
            var_local += 1
        else:
            var_dangling += 1

    # components: real .cn-* retrieved vs cn-looking-but-unknown
    cn_used = set(CN_CLASS.findall(live))
    cn_retrieved = sorted(cn_used & CANON_CN)
    cn_unknown = sorted(cn_used - CANON_CN)

    # icons: library byte-match vs unknown (reuse the gate technique, live html)
    icon_lib_hits = icon_unknown = 0
    for blk in SVGRE.findall(live):
        if "data-bespoke" in blk[: blk.find(">") + 1]:
            continue
        paths = DRE.findall(blk)
        for d in paths:
            if norm(d) in ICON_LIB:
                icon_lib_hits += 1
            else:
                icon_unknown += 1
        if not paths and SHAPERE.search(blk):
            icon_unknown += 1

    candidates = len(CANDIDATE.findall(raw))

    # ---- coarse retrieval posture ----
    if not canon_linked and not cn_retrieved:
        posture = "INVENTED"        # freehand — no canon linkage at all
    elif len(hex_live) == 0 and var_local == 0 and cn_retrieved:
        posture = "PURE-RETRIEVAL"  # every brand value traces to canon
    elif canon_linked or cn_retrieved:
        posture = "HYBRID"          # linked but some invented values leaked in
    else:
        posture = "INVENTED"

    return {
        "file": os.path.basename(path),
        "posture": posture,
        "canon_linked": canon_linked,
        "components_retrieved": len(cn_retrieved),
        "components_list": cn_retrieved,
        "components_unknown": cn_unknown,
        "hex_live": len(hex_live),
        "hex_values": sorted(set(hex_live)),
        "var_canon": var_canon,
        "var_local": var_local,
        "var_dangling": var_dangling,
        "icon_library": icon_lib_hits,
        "icon_unknown": icon_unknown,
        "candidates": candidates,
    }


def collect(spec):
    """spec = file or dir. Returns list of html paths."""
    if os.path.isdir(spec):
        return sorted(glob.glob(os.path.join(spec, "*.html")))
    return [spec] if os.path.exists(spec) else []


def default_lineages():
    ft = os.path.join(HERE, "_fitness-test")
    return {
        "governed-Sonnet": os.path.join(ft, "register-spread-2026-07-05"),
        "governed-Opus": os.path.join(ft, "register-spread-2026-07-05-opus"),
        "diagnostic": os.path.join(ft, "register-spread-2026-07-05-diagnostic"),
    }


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    want_json = "--json" in sys.argv[1:]

    if args:
        lineages = {}
        for a in args:
            if "=" in a:
                label, p = a.split("=", 1)
                lineages[label] = p if os.path.isabs(p) else os.path.join(HERE, p)
    else:
        lineages = default_lineages()

    result = {}
    for label, spec in lineages.items():
        files = collect(spec)
        result[label] = [trace_file(f) for f in files]

    # ---- markdown report ----
    L = [
        "# Knowledge-usage trace — retrieved vs invented (reconstructed from artifacts)",
        "",
        "*Generated by `_trace_knowledge_usage.py`. Measures, per generated screen, how much of what "
        "reads-as-brand was RETRIEVED from the knowledge base (canon.css tokens/`.cn-*` components, "
        "byte-matched icons) vs INVENTED free-hand (live hex, local-only palette vars, unknown icons). "
        "Colour is a §9 CARDINAL curb — it must be retrieved, never typed — so `hex_live > 0` is a "
        "cardinal violation and the headline invention signal. Not a gate; a measurement instrument "
        "for the rules-vs-architecture question.*",
        "",
        f"Canon vocabulary indexed: {len(CANON_VARS)} tokens · {len(CANON_CN)} `.cn-*` components · "
        f"{len(ICON_LIB)} icon glyphs.",
        "",
        "## Per-file trace",
        "",
        "| Lineage | File | Posture | canon? | .cn-* | hex(live) | var·canon | var·local | icon·lib | icon·? | flags |",
        "|---|---|---|:--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    agg = {}
    for label, rows in result.items():
        a = agg.setdefault(label, {"files": 0, "hex": 0, "cn": 0, "vloc": 0, "vcanon": 0,
                                    "iunk": 0, "postures": []})
        for r in rows:
            a["files"] += 1
            a["hex"] += r["hex_live"]
            a["cn"] += r["components_retrieved"]
            a["vloc"] += r["var_local"]
            a["vcanon"] += r["var_canon"]
            a["iunk"] += r["icon_unknown"]
            a["postures"].append(r["posture"])
            L.append(
                f"| {label} | {r['file']} | {r['posture']} | "
                f"{'Y' if r['canon_linked'] else '—'} | {r['components_retrieved']} | "
                f"{r['hex_live']} | {r['var_canon']} | {r['var_local']} | "
                f"{r['icon_library']} | {r['icon_unknown']} | {r['candidates']} |"
            )

    L += ["", "## Per-lineage aggregate", "",
          "| Lineage | files | postures | Σ hex(live) | Σ .cn-* | Σ var·canon | Σ var·local | Σ icon·? |",
          "|---|--:|---|--:|--:|--:|--:|--:|"]
    for label, a in agg.items():
        from collections import Counter
        pc = ", ".join(f"{k}×{v}" for k, v in Counter(a["postures"]).items())
        L.append(f"| {label} | {a['files']} | {pc} | {a['hex']} | {a['cn']} | "
                 f"{a['vcanon']} | {a['vloc']} | {a['iunk']} |")

    L += [
        "",
        "## How to read this",
        "",
        "- **hex(live) & var·local are the invention signals.** High = the screen made up brand "
        "values instead of retrieving them. Colour is cardinal, so live hex is the sharpest tell.",
        "- **.cn-* & var·canon are the retrieval signals.** High = composition and tokens pulled "
        "from the reviewed KB.",
        "- **Posture** collapses this to one word per screen: PURE-RETRIEVAL (all brand values "
        "trace to canon) · HYBRID (linked but leaked invented values) · INVENTED (freehand, no "
        "canon linkage).",
        "- **The rules-vs-architecture read:** if governed lineages already sit near PURE-RETRIEVAL "
        "yet still underwhelm, the ceiling is unlikely to be retrieval-adherence (a rules problem) — "
        "it points at the single-pass architecture. If governed lineages leak inventions the rules "
        "forbade, the rules/prompt-crafting still has room first. Compare the governed columns "
        "against `diagnostic` (deliberately unconstrained) as the invention baseline.",
        "",
        "> Caveat: measures provenance/adherence, NOT layout quality or gestalt (the very thing "
        "Dave judged better when unconstrained). A screen can be PURE-RETRIEVAL and still feel flat, "
        "or INVENTED and feel great. Read alongside the visual verdict, not instead of it.",
    ]
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")

    if want_json:
        json.dump(result, open(OUT_JSON, "w"), indent=2)

    # console summary
    print("Wrote", os.path.relpath(OUT_MD, HERE))
    for label, a in agg.items():
        from collections import Counter
        print(f"  {label:20s} {a['files']} files · Σhex(live)={a['hex']:3d} · "
              f"Σ.cn-*={a['cn']:3d} · Σvar·local={a['vloc']:3d} · "
              f"postures={dict(Counter(a['postures']))}")


if __name__ == "__main__":
    main()
