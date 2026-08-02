#!/usr/bin/env python3
"""Derived-view generators over the knowledge graph (Graphify-inspired, no dependency).

Produces:
  - knowledge/tokens/_blast-radius.json  : token -> [components] reverse index + god-node ranking
  - knowledge/_GRAPH-REPORT.md           : health dashboard (god-nodes, groups, orphans, compliance, depricate)

Token usage is matched by scanning each component meta's `tokens` + `subComponents`
blocks for the exact store token paths (word-boundary safe), so only real tokens count
and prefixes (icon/default vs icon/default-reverse) don't double-match.

Usage:  python3 knowledge/tokens/_build_blast_radius.py             # regenerate (writes both files)
        python3 knowledge/tokens/_build_blast_radius.py --check     # NO WRITE. Recomputes both
                                                                       outputs in memory and compares
                                                                       them BY CONTENT (never mtime)
                                                                       against what's on disk; exits
                                                                       non-zero on ANY drift. This is
                                                                       _GRAPH-REPORT.md's first real
                                                                       reader (#79 P6 — an instrument
                                                                       ships WITH its reader).
        python3 knowledge/tokens/_build_blast_radius.py --selftest  # determinism + drift-detection bites

CAVEAT (#79 P6, same shape as _gen_chain.py's --check — see _build_all.py's note on it): wired
into _build_all.py directly after the unconditional-write step, --check there can only ever prove
compute() is DETERMINISTIC (two renders of the same input agree) — the preceding STEPS entry
already regenerated both files fresh in the same process, so by the time --check runs there is
nothing left to catch. It does NOT by itself catch a _GRAPH-REPORT.md that drifted from source
BETWEEN sessions (tokens/metas edited, generator never rerun) — that needs a second reader at the
commit seam, same as _CHAIN.md's. Flagged, not silently claimed (2026-08-02 periphery finding).
"""
import json, re, glob, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = os.path.join(ROOT, "tokens")
COMP = os.path.join(ROOT, "components")
OUT_JSON = os.path.join(TOK, "_blast-radius.json")
OUT_MD = os.path.join(ROOT, "_GRAPH-REPORT.md")


def compute():
    """Pure — reads the token store + component metas + compliance rollup, returns
    (blast_dict, report_text, extra) and writes NOTHING. Split out of main() (#79 P6)
    so --check can compare this against what's on disk without regenerating it first."""
    # --- token store: all defined leaf paths ---
    store = {}
    def walk(node, path=""):
        if isinstance(node, dict):
            if any(k in node for k in ("$value", "light", "scale-1", "dark")):
                store[path] = True
            for k, v in node.items():
                if k.startswith("$"):
                    continue
                walk(v, (path + "/" + k).strip("/") if path else k)
    for f in glob.glob(os.path.join(TOK, "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            walk(json.load(open(f)))
        except Exception:
            pass
    store_paths = sorted(store, key=len, reverse=True)  # longest first

    # --- scan component metas for token usage ---
    tok_to_comps = defaultdict(set)
    comp_to_toks = defaultdict(set)
    comp_depricate = {}   # component -> count of (depricate) refs in tokens block
    metas = []
    for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
        b = os.path.basename(f)
        if b.startswith("EXAMPLE"):
            continue
        d = json.load(open(f))
        name = d.get("name", b)
        metas.append(name)
        blob = json.dumps(d.get("tokens", {})) + json.dumps(d.get("subComponents", {})) + json.dumps(d.get("variants", []))
        for p in store_paths:
            if re.search(r"(?<![\w/-])" + re.escape(p) + r"(?![\w/-])", blob):
                tok_to_comps[p].add(name)
                comp_to_toks[name].add(p)
        dep = len(re.findall(r"\(depricate\)", blob))
        if dep:
            comp_depricate[name] = dep

    # --- blast-radius index ---
    ranking = sorted(tok_to_comps.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    blast = {
        "$description": "Token blast-radius index — which components reference each live token (god-nodes = highest blast radius). Generated from component meta `tokens` blocks vs the token store. Use before changing/rebinding a token to see what's affected. Conformance: derived view, regenerate after meta/token edits.",
        "generated": "2026-06-18",
        "totals": {"tokens_defined": len(store), "tokens_referenced": len(tok_to_comps), "components": len(metas)},
        "ranking": [{"token": t, "blast": len(c), "components": sorted(c)} for t, c in ranking],
        "by_component": {c: sorted(list(s)) for c, s in sorted(comp_to_toks.items())},
    }

    # --- token group coverage ---
    def group(p):
        return p.split("/")[0]
    grp_comps = defaultdict(set)
    for t, cs in tok_to_comps.items():
        grp_comps[group(t)] |= cs
    grp_rank = sorted(grp_comps.items(), key=lambda kv: -len(kv[1]))

    # --- orphans: defined leaf tokens never referenced by any component ---
    referenced = set(tok_to_comps)
    orphans = sorted(set(store) - referenced)
    orphan_groups = Counter(group(p) for p in orphans)

    # --- compliance rollup (from graph-index if present) ---
    gi_path = os.path.join(ROOT, "compliance", "graph-index.json")
    comp_rules = ""
    if os.path.exists(gi_path):
        gi = json.load(open(gi_path))
        comp_rules = f"{gi['totals']['rules']} rules x {gi['totals']['components']} components ({gi['totals']['sc']} SCs)"

    # --- write report ---
    top = ranking[:15]
    L = []
    L.append("# Knowledge graph — health report")
    L.append("")
    L.append("> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.")
    L.append("")
    L.append(f"**Totals:** {len(metas)} components · {len(store)} tokens defined · {len(tok_to_comps)} tokens referenced by components · compliance: {comp_rules or 'n/a'}.")
    L.append("")
    L.append("## God-nodes — highest token blast radius")
    L.append("")
    L.append("Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).")
    L.append("")
    L.append("| Token | Blast | Example components |")
    L.append("|---|---|---|")
    for t, c in top:
        ex = ", ".join(sorted(c)[:6]) + ("…" if len(c) > 6 else "")
        L.append(f"| `{t}` | {len(c)} | {ex} |")
    L.append("")
    L.append("## Token-group reach (components using each group)")
    L.append("")
    L.append("| Group | Components |")
    L.append("|---|---|")
    for g, c in grp_rank:
        L.append(f"| `{g}/` | {len(c)} |")
    L.append("")
    L.append("## Deprecated tokens still bound (migration worklist)")
    L.append("")
    if comp_depricate:
        L.append("Components whose `tokens` block still references a `(depricate)` token (count = mentions). See `tokens/_manifests/depricate-replacement-map.json` `$usage_audit` for the rebind targets and `_DESIGN-SYSTEM-GAPS.md` for blockers.")
        L.append("")
        L.append("| Component | (depricate) refs |")
        L.append("|---|---|")
        for c, n in sorted(comp_depricate.items(), key=lambda kv: -kv[1]):
            L.append(f"| {c} | {n} |")
    else:
        L.append("None — all components migrated off deprecated tokens. 🎉")
    L.append("")
    L.append("## Orphans — defined tokens not referenced by any component meta")
    L.append("")
    L.append(f"{len(orphans)} of {len(store)} defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:")
    L.append("")
    L.append("| Group | Unreferenced |")
    L.append("|---|---|")
    for g, n in orphan_groups.most_common():
        L.append(f"| `{g}/` | {n} |")
    L.append("")
    L.append("> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.")
    L.append("")
    report_text = "\n".join(L)

    extra = {
        "store": len(store), "tok_to_comps": len(tok_to_comps), "metas": len(metas),
        "top8": [(t, len(c)) for t, c in top[:8]],
        "comp_depricate": len(comp_depricate), "orphans": len(orphans),
    }
    return blast, report_text, extra


def write(blast, report_text):
    json.dump(blast, open(OUT_JSON, "w"), indent=2, ensure_ascii=False)
    open(OUT_MD, "w").write(report_text)


def diff_against_disk(blast, report_text, out_json_path=None, out_md_path=None):
    """Content compare (never mtime — this project has ruled mtime comparisons
    unacceptable) of a freshly computed (blast, report_text) against whatever is
    CURRENTLY on disk at out_json_path / out_md_path (default: the real generated
    files). Returns a list of human-readable mismatch strings; an empty list means
    in sync. Pure — never writes. #79 P6: this is what makes _GRAPH-REPORT.md and
    its json sibling readable-and-failable rather than write-only."""
    out_json_path = out_json_path or OUT_JSON
    out_md_path = out_md_path or OUT_MD
    problems = []

    expected_json_text = json.dumps(blast, indent=2, ensure_ascii=False)
    if not os.path.exists(out_json_path):
        problems.append(f"{out_json_path} does not exist — never generated")
    else:
        on_disk = open(out_json_path, encoding="utf-8").read()
        if on_disk != expected_json_text:
            problems.append(
                f"{out_json_path} content differs from a fresh compute() "
                f"(disk {len(on_disk)} bytes vs fresh {len(expected_json_text)} bytes) — "
                f"stale: tokens/components changed without regenerating, or the file was hand-edited")

    if not os.path.exists(out_md_path):
        problems.append(f"{out_md_path} does not exist — never generated")
    else:
        on_disk = open(out_md_path, encoding="utf-8").read()
        if on_disk != report_text:
            disk_lines, fresh_lines = on_disk.split("\n"), report_text.split("\n")
            n = min(len(disk_lines), len(fresh_lines))
            first_diff = next((i for i in range(n) if disk_lines[i] != fresh_lines[i]), n)
            disk_ln = disk_lines[first_diff] if first_diff < len(disk_lines) else "<EOF>"
            fresh_ln = fresh_lines[first_diff] if first_diff < len(fresh_lines) else "<EOF>"
            problems.append(
                f"{out_md_path} content differs from a fresh compute() at line {first_diff + 1}: "
                f"disk={disk_ln!r} vs fresh={fresh_ln!r}")

    return problems


def selftest():
    """#79 P6 — _GRAPH-REPORT.md's first real bites.
    (a) determinism     — compute() called twice yields byte-identical output.
    (b1) quiet-on-match — diff_against_disk() reports zero problems against a fixture
         pair that IS a fresh compute()'s output.
    (b2) bites-on-drift — a doctored fixture pair (both files touched) is flagged on
         BOTH files, each message naming the doctored path.
    (b3) missing-file   — a fixture path that doesn't exist is flagged, never silently
         treated as a match.
    All fixtures live under tempfile.mkdtemp(); nothing under the repo is touched."""
    import tempfile, shutil
    blast1, report1, _ = compute()
    blast2, report2, _ = compute()
    assert blast1 == blast2 and report1 == report2, \
        "selftest (a): compute() is non-deterministic — two calls produced different output"
    print("  selftest (a): compute() is deterministic across two calls ✓")

    tmpdir = tempfile.mkdtemp(prefix="blast-radius-selftest-")
    try:
        good_json, good_md = os.path.join(tmpdir, "good.json"), os.path.join(tmpdir, "good.md")
        json.dump(blast1, open(good_json, "w"), indent=2, ensure_ascii=False)
        open(good_md, "w").write(report1)
        problems = diff_against_disk(blast1, report1, out_json_path=good_json, out_md_path=good_md)
        assert problems == [], f"selftest (b1): matching fixture flagged as drifted: {problems}"
        print("  selftest (b1): identical fixture pair reports zero drift ✓")

        bad_json, bad_md = os.path.join(tmpdir, "bad.json"), os.path.join(tmpdir, "bad.md")
        doctored = dict(blast1)
        doctored["totals"] = dict(blast1["totals"])
        doctored["totals"]["components"] = blast1["totals"]["components"] + 1
        json.dump(doctored, open(bad_json, "w"), indent=2, ensure_ascii=False)
        open(bad_md, "w").write(report1.replace("# Knowledge graph", "# Knowledge graph (HAND-EDITED)", 1))
        problems = diff_against_disk(blast1, report1, out_json_path=bad_json, out_md_path=bad_md)
        assert len(problems) == 2, f"selftest (b2): doctored fixture pair should flag BOTH files: {problems}"
        assert any("bad.json" in p for p in problems) and any("bad.md" in p for p in problems), \
            f"selftest (b2): mismatch messages don't name the doctored files: {problems}"
        print("  selftest (b2): a doctored fixture pair is flagged on BOTH files, each named ✓")

        missing_json = os.path.join(tmpdir, "does-not-exist.json")
        problems = diff_against_disk(blast1, report1, out_json_path=missing_json, out_md_path=good_md)
        assert len(problems) == 1 and "does not exist" in problems[0], \
            f"selftest (b3): missing file was not flagged: {problems}"
        print("  selftest (b3): a missing on-disk file is flagged, never silently treated as a match ✓")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("selftest PASS — compute() deterministic; --check bites on drift, quiet on a match, "
          "never silently passes a missing file (#79 P6)")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()

    blast, report_text, extra = compute()

    if "--check" in argv:
        problems = diff_against_disk(blast, report_text)
        if problems:
            print(f"❌ _build_blast_radius --check FAILED — {len(problems)} file(s) out of sync with a fresh compute():")
            for p in problems:
                print(f"  - {p}")
            print("  Fix: python3 knowledge/tokens/_build_blast_radius.py")
            return 1
        print("✓ _build_blast_radius --check PASS — tokens/_blast-radius.json and _GRAPH-REPORT.md "
              "match a fresh compute() (content, not mtime)")
        return 0

    write(blast, report_text)
    print("wrote tokens/_blast-radius.json and _GRAPH-REPORT.md")
    print(f"tokens defined={extra['store']} referenced={extra['tok_to_comps']} components={extra['metas']}")
    print("top god-nodes:", extra["top8"])
    print("depricate-still-bound components:", extra["comp_depricate"])
    print("orphans:", extra["orphans"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
