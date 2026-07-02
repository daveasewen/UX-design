#!/usr/bin/env python3
"""Icon contrast delta — brand 4.5:1 vs WCAG 3:1 (ADVISORY; sizes the promotion).

WHY (icon-015 / col26-007, ingested 2026-07-02): the 2026 brand standard wants
icons at 4.5:1 "in all instances" (interactive, legibility-critical); our gates
pass icons at the WCAG 1.4.11 floor of 3:1. Pictograms (3:1 + alt) and chart/RAG
indicators (3:1) are NOT covered by the stricter rule — asset-class split per
the icons standard. Dave ruling 2026-07-02: build ADVISORY-FIRST, get the real
failure count, THEN rule on promotion (ADR-0005 §5 path).

What it measures — the DEAD ZONE (≥3:1 but <4.5:1), i.e. combos that pass
today's gate but would fail the brand rule:

  1. DECLARED icon pairs — snippet-manifest contrastPairs whose fg is an icon/*
     token, both modes. The concrete promotion cost.
  2. EXHAUSTIVE icon/* × every background/surface token × both modes — the
     state-contrast lesson (declared pairs hide undeclared combos). UPPER BOUND:
     co-occurrence isn't guaranteed; a dead-zone combo here means "check whether
     this icon can ever sit on this surface", not "defect".
  3. CLASSIFY queue — ui-context pairs whose fg is rag/* (some are true icon
     glyphs, e.g. Notification icons → brand 4.5 would apply; some are
     indicators → 3:1 stands). Needs a human class call per pair.

Writes knowledge/_ICON-CONTRAST-DELTA.md. ALWAYS exits 0 — advisory annotates,
never blocks. Promotion would move the 4.5 threshold for class-'icon' pairs
into _validate_snippets.py (+ bite-test), same route as the all-caps check.
"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import contrast_ratio, CONTRAST_ALLOWLIST

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")
BRAND, WCAG = 4.5, 3.0

sem = json.load(open(os.path.join(TOK, "semantic-colour.json")))


def leaves(node, path="", out=None):
    if out is None:
        out = {}
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "dark")):
            out[path] = node
            return out
        for k, v in node.items():
            if not k.startswith("$"):
                leaves(v, (path + "/" + k).strip("/") if path else k, out)
    return out


LEAVES = leaves(sem)


def value(token, mode):
    n = LEAVES.get(token)
    if n is None:
        return None
    m = n.get(mode, n.get("$value"))
    v = m.get("$value") if isinstance(m, dict) else m
    return v.upper() if isinstance(v, str) and v.startswith("#") and len(v) in (7, 9) else None


def bucket(r):
    if r is None:
        return "unresolved"
    if r >= BRAND:
        return "pass-4.5"
    if r >= WCAG:
        return "DEAD-ZONE"
    return "below-3(gated)"


def pair_rows(fg, bg):
    rows = []
    for mode in ("light", "dark"):
        f, b = value(fg, mode), value(bg, mode)
        if f and b and (len(f) == 9 or len(b) == 9):
            # alpha channel present → surface is composite (e.g. transparent form
            # background); true contrast depends on what's underneath. Render-path work.
            rows.append((fg, bg, mode, None, "transparent(composite)"))
            continue
        r = round(contrast_ratio(f, b), 2) if f and b else None
        rows.append((fg, bg, mode, r, bucket(r)))
    return rows


# 1. declared icon pairs from snippet manifests
declared, classify = [], []
for p in sorted(glob.glob(os.path.join(ROOT, "snippets", "*.reference.html"))):
    html = open(p).read()
    mm = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
    if not mm:
        continue
    try:
        man = json.loads(mm.group(1))
    except Exception:
        continue
    name = os.path.basename(p)
    for pr in man.get("contrastPairs", []):
        fg, bg = pr.get("fg", ""), pr.get("bg", "")
        if fg.startswith("icon/") or "/icon" in fg:
            declared += [(name,) + row for row in pair_rows(fg, bg)]
        elif pr.get("context") == "ui" and fg.startswith("rag/"):
            classify += [(name,) + row for row in pair_rows(fg, bg)]

# 2. exhaustive icon/* × surfaces × modes
icon_tokens = sorted(k for k in LEAVES if k.startswith("icon/"))
surfaces = sorted(k for k in LEAVES
                  if any(s in k for s in ("background", "surface"))
                  and not any(x in k for x in ("on-light", "on-dark")))
exhaustive = []
for it in icon_tokens:
    for s in surfaces:
        exhaustive += pair_rows(it, s)

dz_decl = [r for r in declared if r[5] == "DEAD-ZONE"]
dz_exh = [r for r in exhaustive if r[4] == "DEAD-ZONE"]
dz_cls = [r for r in classify if r[5] == "DEAD-ZONE"]


def fmt(rows, with_file):
    out = []
    for r in rows:
        if with_file:
            f, fg, bg, mode, ratio, b = r
            allowed = " (allowlisted)" if fg in CONTRAST_ALLOWLIST else ""
            out.append(f"| {f} | {fg}{allowed} | {bg} | {mode} | {ratio} | {b} |")
        else:
            fg, bg, mode, ratio, b = r
            allowed = " (allowlisted)" if fg in CONTRAST_ALLOWLIST else ""
            out.append(f"| {fg}{allowed} | {bg} | {mode} | {ratio} | {b} |")
    return out


lines = [
    "# Icon contrast delta — brand 4.5:1 vs gate 3:1 (ADVISORY)",
    "",
    "*Generated by `_build_icon_contrast_delta.py`. Sizes the icon-015 promotion",
    "(Dave ruling 2026-07-02: advisory-first). DEAD-ZONE = passes today's 3:1 gate,",
    "fails the brand 4.5:1. Never blocks.*",
    "",
    f"**Headline: {len(dz_decl)} declared · {len(dz_exh)} exhaustive (upper bound) · "
    f"{len(dz_cls)} awaiting icon-vs-indicator classification.**",
    "",
    "## 1. Declared icon pairs (the concrete promotion cost)",
    "",
    "| snippet | fg | bg | mode | ratio | verdict |",
    "|---|---|---|---|---|---|",
] + (fmt(declared, True) or ["| — | — | — | — | — | none declared |"]) + [
    "",
    "## 2. Exhaustive icon/* × surfaces (upper bound — verify co-occurrence before treating as defect)",
    "",
    "| fg | bg | mode | ratio | verdict |",
    "|---|---|---|---|---|",
] + fmt([r for r in exhaustive if r[4] not in ("pass-4.5", "transparent(composite)")], False) + [
    "",
    f"_({sum(1 for r in exhaustive if r[4] == 'pass-4.5')} of {len(exhaustive)} exhaustive combos already clear 4.5:1; "
    f"{sum(1 for r in exhaustive if r[4] == 'transparent(composite)')} transparent/composite surfaces skipped "
    f"(alpha — true contrast needs the render path) — omitted.)_",
    "",
    "## 3. Classification queue — rag/* used in ui context (icon glyph or indicator?)",
    "",
    "| snippet | fg | bg | mode | ratio | verdict |",
    "|---|---|---|---|---|---|",
] + (fmt(classify, True) or ["| — | — | — | — | — | none found |"]) + [
    "",
    "Icon glyphs (e.g. Notification leading icons) take brand 4.5 on promotion;",
    "indicators (Status dots, chart marks) stay 3:1 per the asset-class split (icon-015).",
]

open(os.path.join(ROOT, "_ICON-CONTRAST-DELTA.md"), "w").write("\n".join(lines) + "\n")
print(f"icon contrast delta: {len(dz_decl)} declared dead-zone, {len(dz_exh)} exhaustive (upper bound), "
      f"{len(dz_cls)} to classify — see _ICON-CONTRAST-DELTA.md (advisory)")
sys.exit(0)
