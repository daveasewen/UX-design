#!/usr/bin/env python3
"""_validate_kg.py — parse-gate v1 for the component KG edge layer.

Ruling: s131-D2 (RULED #131) + s133-D1 (RULED #133 scope widening). This is
the "gate-PARSED" requirement s131-D2 sets, and the "nothing re-checks it"
freshness remedy — the class named in knowledge/_NO-GATE-PARSES-THE-ARTEFACT
(no-gate-parses-the-artefact.md): a claim can be true when written and silently
go false with nothing to catch it. This script is that catch, for the `edges`
field minted by knowledge/gen_kg_edges.py.

Checks, all BY ADDITION — this script only reads the corpus, it never edits it:
  (a) every meta's `edges` field parses in the consumer's grammar: every
      non-null ref matches the node-id grammar
      component:|pattern:|context:|snippet:|ruling: and RESOLVES —
        component: against the component meta stems (+ _proforma)
        pattern:/context: against the two node registries
        snippet: against knowledge/snippets/*.reference.html
        ruling: against knowledge/_rulings.json ids (both `rulings` and
                any `_README` entries carrying an id)
  (b) ref:null is legal ONLY paired with a non-empty $note (declared prose
      awaiting a Dave's-eye migration) — counted and reported, never failed.
  (c) a NEW meta — any meta.json under knowledge/components/ (or the
      _proforma dir) that lacks a top-level `provenance` key — is refused.
  (d) `edges`, where present, is checked against the edge definition in
      knowledge/components/meta.schema.json (structural: object of known
      edge-type keys, each an array of {"ref": str|null, "$note"?: str},
      no unknown edge-type keys, no unknown keys inside an edge).
  (e) freshness: knowledge/gen_kg_edges.py must be IDEMPOTENT-CLEAN — it is
      re-run against a scratch copy of the corpus and the result diffed
      against the live corpus. Any drift is a FAIL naming the file(s) that
      differ (the "nothing re-checks it" remedy: this is the something).
      The scratch tree carries the resolutions input too (see (f)) — the
      generator now REFUSES to build without it.
  (f) resolutions CONSUMED (s135-D4): the ruled verdicts file
      reviews/KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json is a generator input.
      This check re-derives the ruled facts from that file INDEPENDENTLY of
      gen_kg_edges.py (it never imports it) and asserts every one of them is
      present in the live corpus:
        MERGE   — no edge anywhere may still carry the merged-away context
                  node-id, and it must not survive in _nodes-context.json
        PROMOTE — the named (meta filename, edge-type, $note) edge must carry
                  the ruled component ref (not null, not something else)
        ATTACH  — the named component must carry governedBy ruling:<rid>
      A build in which the verdicts file is ignored therefore FAILS here.
      Mutation-tested: neuter consumption in gen_kg_edges.py, regenerate,
      and this check goes red.

Exit: rc=1 on ANY structural fail (loud + named: file, edge, reason).
      rc=0 clean. ref:null+$note entries are counted, never a fail.

Usage:
  python3 knowledge/_validate_kg.py             # run the gate on the live corpus
  python3 knowledge/_validate_kg.py --selftest   # synthetic-corpus proof, touches
                                                  # nothing in the live tree
DO-NOT-RULE: this script never closes, converts, merges, or invents an edge.
It reports. Any fix to a ref:null edge or registry content is Dave's-eye
territory per s131-D2/s133-D1's own status lines.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMPONENTS = HERE / "components"
PROFORMA_DIR = HERE / "_proforma"
SNIPPETS = HERE / "snippets"
NODES_PATTERN = COMPONENTS / "_nodes-pattern.json"
NODES_CONTEXT = COMPONENTS / "_nodes-context.json"
RULINGS = HERE / "_rulings.json"
SCHEMA = COMPONENTS / "meta.schema.json"
GEN_SCRIPT = HERE / "gen_kg_edges.py"
RESOLUTIONS = ROOT / "reviews" / "KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json"

REF_RE = re.compile(r"^(component|pattern|context|snippet|ruling):.+$")
NODE_KINDS = ("component", "pattern", "context", "snippet", "ruling")


# --------------------------------------------------------------- corpus load

def load_schema_edge_types(schema_path=None):
    schema_path = schema_path or SCHEMA
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    edges_props = schema["properties"]["edges"]["properties"]
    edge_def = schema["definitions"]["edge"]
    return set(edges_props.keys()), set(edge_def["properties"].keys()), set(edge_def.get("required", []))


def collect_component_files(components_dir=None, proforma_dir=None):
    components_dir = components_dir or COMPONENTS
    proforma_dir = proforma_dir or PROFORMA_DIR
    files = sorted(f for f in components_dir.glob("*.meta.json"))
    if proforma_dir.exists():
        files += sorted(proforma_dir.glob("*.meta.json"))
    return files


def component_stems(files):
    """component:<stem> node-ids resolvable against the meta corpus."""
    return {f"component:{f.name[:-len('.meta.json')]}" for f in files}


def registry_ids(path):
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["id"] for entry in data}


def snippet_ids(snippets_dir=None):
    snippets_dir = snippets_dir or SNIPPETS
    if not snippets_dir.exists():
        return set()
    return {f"snippet:{f.name}" for f in snippets_dir.glob("*.reference.html")}


def ruling_ids(rulings_path=None):
    rulings_path = rulings_path or RULINGS
    if not rulings_path.exists():
        return set()
    data = json.loads(rulings_path.read_text(encoding="utf-8"))
    ids = set()
    for key in ("rulings", "_README"):
        for entry in data.get(key, []) or []:
            if isinstance(entry, dict) and entry.get("id"):
                ids.add(f"ruling:{entry['id']}")
    return ids


# ------------------------------------------------------------------ checks

def check_edge_schema(edges, known_edge_types, edge_props, edge_required):
    """(d) structural schema check against meta.schema.json's edge definition.
    Returns a list of reason strings (empty = clean)."""
    reasons = []
    if not isinstance(edges, dict):
        return [f"`edges` is not an object ({type(edges).__name__})"]
    for etype, arr in edges.items():
        if etype not in known_edge_types:
            reasons.append(f"unknown edge-type key '{etype}' (not in meta.schema.json edges.properties)")
            continue
        if not isinstance(arr, list):
            reasons.append(f"edge-type '{etype}' value is not an array")
            continue
        for i, e in enumerate(arr):
            if not isinstance(e, dict):
                reasons.append(f"{etype}[{i}] is not an object")
                continue
            extra = set(e.keys()) - edge_props
            if extra:
                reasons.append(f"{etype}[{i}] has keys not in the edge definition: {sorted(extra)}")
            missing = edge_required - set(e.keys())
            if missing:
                reasons.append(f"{etype}[{i}] missing required key(s): {sorted(missing)}")
            if "ref" in e and not (e["ref"] is None or isinstance(e["ref"], str)):
                reasons.append(f"{etype}[{i}].ref is not string|null")
            if "$note" in e and not isinstance(e["$note"], str):
                reasons.append(f"{etype}[{i}].$note is not a string")
    return reasons


def resolve_ref(ref, resolvers):
    """ref matches the node-id grammar AND resolves against the right registry."""
    if not REF_RE.match(ref):
        return False, "ref does not match node-id grammar 'kind:rest' for kind in " + "|".join(NODE_KINDS)
    kind = ref.split(":", 1)[0]
    if ref not in resolvers[kind]:
        return False, f"ref does not resolve — no such {kind} node"
    return True, None


def validate_corpus(components_dir=None, proforma_dir=None, snippets_dir=None,
                     nodes_pattern_path=None, nodes_context_path=None, rulings_path=None,
                     schema_path=None):
    """Runs checks (a)(b)(c)(d) against a corpus rooted at the given dirs
    (defaults = the live corpus). Returns (fails, null_note_count, files_checked)."""
    components_dir = components_dir or COMPONENTS
    proforma_dir = proforma_dir or PROFORMA_DIR
    snippets_dir = snippets_dir or SNIPPETS
    nodes_pattern_path = nodes_pattern_path or NODES_PATTERN
    nodes_context_path = nodes_context_path or NODES_CONTEXT
    rulings_path = rulings_path or RULINGS
    schema_path = schema_path or SCHEMA

    known_edge_types, edge_props, edge_required = load_schema_edge_types(schema_path)

    files = collect_component_files(components_dir, proforma_dir)
    comp_ids = component_stems(files)
    resolvers = {
        "component": comp_ids,
        "pattern": registry_ids(nodes_pattern_path),
        "context": registry_ids(nodes_context_path),
        "snippet": snippet_ids(snippets_dir),
        "ruling": ruling_ids(rulings_path),
    }

    fails = []
    null_note_count = 0

    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            fails.append(f"{f}: FAIL — unparseable JSON ({e})")
            continue

        # (c) provenance required — refuse a NEW meta lacking it
        if "provenance" not in data:
            fails.append(f"{f}: FAIL — no `provenance` field (new/incomplete metas are refused)")

        edges = data.get("edges")
        if edges is None:
            continue  # no edges field: nothing to parse (legal — e.g. EXAMPLE-button)

        # (d) schema check
        for reason in check_edge_schema(edges, known_edge_types, edge_props, edge_required):
            fails.append(f"{f}: FAIL — edges schema — {reason}")
        if not isinstance(edges, dict):
            continue

        # (a)(b) per-edge ref parse + resolve, or null+$note
        for etype, arr in edges.items():
            if etype not in known_edge_types or not isinstance(arr, list):
                continue  # already reported by the schema check above
            for i, e in enumerate(arr):
                if not isinstance(e, dict) or "ref" not in e:
                    continue  # already reported
                ref = e.get("ref")
                if ref is None:
                    note = e.get("$note")
                    if not note or not str(note).strip():
                        fails.append(f"{f}: FAIL — {etype}[{i}] ref:null with no (or empty) $note")
                    else:
                        null_note_count += 1
                    continue
                ok, reason = resolve_ref(ref, resolvers)
                if not ok:
                    fails.append(f"{f}: FAIL — {etype}[{i}] ref='{ref}' — {reason}")

    return fails, null_note_count, len(files)


# --------------------------------------------------------------- freshness

def check_freshness():
    """(e) gen_kg_edges.py must be idempotent-clean: regenerate to a scratch
    copy of the whole corpus it touches and diff against the live tree.
    Drift = FAIL naming the file(s)."""
    fails = []
    with tempfile.TemporaryDirectory(prefix="kg-freshness-") as td:
        tdp = Path(td)
        scratch_knowledge = tdp / "knowledge"
        scratch_knowledge.mkdir()
        # gen_kg_edges.py addresses ROOT / "components", ROOT / "_proforma",
        # ROOT / "snippets" via Path(__file__).resolve().parent — so build a
        # scratch tree with the same relative layout and point a copy of the
        # script's ROOT there by copying the whole knowledge/ dir minus the
        # things it doesn't touch (cheap: it's json + one dir of html).
        for name in ("components", "_proforma", "snippets"):
            src = HERE / name
            if src.exists():
                shutil.copytree(src, scratch_knowledge / name)
        scratch_gen = scratch_knowledge / "gen_kg_edges.py"
        shutil.copy2(GEN_SCRIPT, scratch_gen)
        # s135-D4: the generator addresses its resolutions input at
        # ROOT.parent / "reviews" / <name> — mirror that into the scratch tree
        # or the regeneration REFUSES (which is the correct refusal, but here
        # it would mask the freshness question we are actually asking).
        if RESOLUTIONS.exists():
            scratch_reviews = tdp / "reviews"
            scratch_reviews.mkdir(exist_ok=True)
            shutil.copy2(RESOLUTIONS, scratch_reviews / RESOLUTIONS.name)

        proc = subprocess.run(
            [sys.executable, str(scratch_gen)],
            cwd=str(scratch_knowledge), capture_output=True, text=True, timeout=90,
        )
        if proc.returncode != 0:
            fails.append(
                f"gen_kg_edges.py: FAIL — regeneration on a scratch copy exited "
                f"{proc.returncode} (stderr: {proc.stderr.strip()[:500]})"
            )
            return fails

        # diff every file gen_kg_edges.py can touch: all component metas,
        # proforma, and the two registries.
        live_files = collect_component_files() + [NODES_PATTERN, NODES_CONTEXT]
        for lf in live_files:
            if lf.is_relative_to(PROFORMA_DIR):
                rel = Path("_proforma") / lf.name
            elif lf.is_relative_to(COMPONENTS):
                rel = Path("components") / lf.name
            else:
                continue
            scratch_f = scratch_knowledge / rel
            if not scratch_f.exists():
                fails.append(f"gen_kg_edges.py freshness: FAIL — {lf} missing from regenerated scratch copy")
                continue
            live_text = lf.read_text(encoding="utf-8")
            scratch_text = scratch_f.read_text(encoding="utf-8")
            if live_text != scratch_text:
                fails.append(
                    f"gen_kg_edges.py freshness: FAIL — {lf} DRIFTED from a clean "
                    f"regeneration (gen_kg_edges.py is not idempotent-clean on this file; "
                    f"regenerate and commit, or investigate non-determinism)"
                )
    return fails


# ------------------------------------------------------- (f) consumed check

def check_resolutions_consumed(components_dir=None, proforma_dir=None,
                               nodes_context_path=None, resolutions_path=None):
    """(f) s135-D4 — assert the ruled verdicts file was CONSUMED by the build.

    Deliberately does NOT import or inspect gen_kg_edges.py: it re-derives the
    ruled facts straight from the verdicts file and looks for them in the live
    corpus. That way it gates the PRESENCE of the resolutions, not the shape of
    whatever code claims to apply them — a build that ignores the file fails
    here regardless of how it ignored it.

    Returns (fails, counts). Parse problems fail LOUD and NAMED, never default.
    """
    components_dir = components_dir or COMPONENTS
    proforma_dir = proforma_dir or PROFORMA_DIR
    nodes_context_path = nodes_context_path or NODES_CONTEXT
    resolutions_path = resolutions_path or RESOLUTIONS

    counts = {"merge": 0, "promote": 0, "attach": 0}
    if not resolutions_path.exists():
        return ([f"resolutions: FAIL — {resolutions_path} MISSING — s135-D4 makes it a "
                 f"generator input; without it no ruled verdict can be shown to have landed"],
                counts)
    try:
        raw = json.loads(resolutions_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("top level is not an object")
        for section in ("nearmiss", "prose", "governed"):
            if not isinstance(raw.get(section), list):
                raise ValueError(f"section '{section}' missing or not a list")
    except Exception as e:
        return ([f"resolutions: FAIL — {resolutions_path} UNREADABLE/MALFORMED ({e!r}) — "
                 f"refusing to report consumption from a file this gate could not parse"], counts)

    files = collect_component_files(components_dir, proforma_dir)
    metas = {}
    for f in files:
        try:
            metas[f] = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue  # already failed loudly in validate_corpus()

    fails = []

    # --- MERGE: the merged-away context node must be GONE, everywhere -------
    merged_nodes = {r["node"] for r in raw["nearmiss"]
                    if r.get("verdict") == "MERGE" and r.get("node")}
    ctx_ids = registry_ids(nodes_context_path)
    for node in sorted(merged_nodes):
        counts["merge"] += 1
        if node in ctx_ids:
            fails.append(f"resolutions: FAIL — MERGE {node} NOT CONSUMED — the node is still "
                         f"registered in {nodes_context_path.name}")
        holders = sorted({f.name for f, d in metas.items()
                          for arr in (d.get("edges") or {}).values() if isinstance(arr, list)
                          for e in arr if isinstance(e, dict) and e.get("ref") == node})
        if holders:
            fails.append(f"resolutions: FAIL — MERGE {node} NOT CONSUMED — still referenced by "
                         f"{len(holders)} meta(s): {holders[:5]}")

    # --- PROMOTE: the named edge must carry the ruled ref -------------------
    for r in raw["prose"]:
        verdict = r.get("verdict") or ""
        if not verdict.startswith("PROMOTE"):
            continue
        counts["promote"] += 1
        fname, grp, note = r.get("file"), r.get("grp"), r.get("note")
        if not (fname and grp and note):
            fails.append(f"resolutions: FAIL — malformed prose PROMOTE row (missing file/grp/note): {r!r}")
            continue
        seen = False
        for f, d in metas.items():
            if f.name != fname:
                continue
            for e in (d.get("edges") or {}).get(grp, []) or []:
                if isinstance(e, dict) and e.get("$note") == note:
                    seen = True
                    if not e.get("ref"):
                        fails.append(f"resolutions: FAIL — PROMOTE NOT CONSUMED — {f.name} / {grp} / "
                                     f"$note={note[:60]!r} still has ref:{e.get('ref')!r} "
                                     f"(verdict '{verdict}')")
        if not seen:
            fails.append(f"resolutions: FAIL — PROMOTE UNMATCHED — no edge {fname} / {grp} with "
                         f"$note={note[:60]!r} exists in the corpus (verdicts file is stale)")

    # --- ATTACH: governedBy must carry the ruled ruling --------------------
    for r in raw["governed"]:
        if r.get("verdict") != "ATTACH":
            continue
        counts["attach"] += 1
        comp, rid = r.get("comp"), r.get("rid")
        if not (comp and rid):
            fails.append(f"resolutions: FAIL — malformed governed ATTACH row (missing comp/rid): {r!r}")
            continue
        want = f"ruling:{rid}"
        targets = [d for f, d in metas.items() if f.name == f"{comp}.meta.json"]
        if not targets:
            fails.append(f"resolutions: FAIL — ATTACH UNMATCHED — no meta '{comp}.meta.json' "
                         f"in the corpus (verdicts file is stale)")
            continue
        if not any(any(isinstance(e, dict) and e.get("ref") == want
                       for e in (d.get("edges") or {}).get("governedBy", []) or [])
                   for d in targets):
            fails.append(f"resolutions: FAIL — ATTACH NOT CONSUMED — {comp}.meta.json carries no "
                         f"governedBy edge '{want}'")

    return fails, counts


# --------------------------------------------------------------------- main

def run_gate():
    print("== _validate_kg.py — KG edge parse-gate (s131-D2 / s133-D1 / s135-D4) ==")
    fails, null_note_count, n_files = validate_corpus()
    fresh_fails = check_freshness()
    fails += fresh_fails
    res_fails, res_counts = check_resolutions_consumed()
    fails += res_fails

    print(f"metas checked: {n_files}")
    print(f"ref:null + $note (declared, awaiting Dave's-eye migration): {null_note_count}")
    print(f"resolutions consumed (s135-D4, {RESOLUTIONS.name}): "
          f"{sum(res_counts.values())} ruled verdicts asserted present "
          f"(MERGE {res_counts['merge']} / PROMOTE {res_counts['promote']} / ATTACH {res_counts['attach']})")
    if fails:
        print(f"\n{len(fails)} FAIL(s):")
        for f in fails:
            print(f"  ✗ {f}")
        print("\n_validate_kg.py: FAIL")
        return 1
    print("\n_validate_kg.py: OK — every ref parses+resolves, every null carries a note, "
          "every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, "
          "and the s135-D4 resolutions input was consumed.")
    return 0


# ------------------------------------------------------------------ selftest

def selftest():
    """Builds a tiny synthetic corpus in a temp dir (never touches the live
    tree) and asserts three arms:
      1. a deliberately broken ref FAILS
      2. a legal ref:null + $note PASSES
      3. a meta missing `provenance` FAILS
    """
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    with tempfile.TemporaryDirectory(prefix="kg-selftest-") as td:
        tdp = Path(td)
        components_dir = tdp / "components"
        proforma_dir = tdp / "_proforma"  # left empty — legal, collect_component_files handles it
        snippets_dir = tdp / "snippets"
        components_dir.mkdir()
        snippets_dir.mkdir()

        # a resolvable snippet target
        (snippets_dir / "Widget.reference.html").write_text("<div></div>", encoding="utf-8")

        nodes_pattern_path = tdp / "_nodes-pattern.json"
        nodes_context_path = tdp / "_nodes-context.json"
        nodes_pattern_path.write_text(json.dumps([{"id": "pattern:demo", "label": "Demo", "sources": []}]), encoding="utf-8")
        nodes_context_path.write_text(json.dumps([]), encoding="utf-8")

        rulings_path = tdp / "_rulings.json"
        rulings_path.write_text(json.dumps({"_README": [], "rulings": [{"id": "s999-D1"}]}), encoding="utf-8")

        schema_path = SCHEMA  # the real schema — this is the grammar under test

        # --- meta A: everything legal ---------------------------------
        meta_a = {
            "name": "Widget", "category": "atom", "purpose": "x", "props": [],
            "tokens": {}, "relationships": {}, "accessibility": {"relatedSC": []},
            "antiPatterns": [], "tokenValidation": {"date": "2026-01-01", "against": "x", "result": "ok"},
            "provenance": {"source": "code"},
            "edges": {
                "renderedBy": [{"ref": "snippet:Widget.reference.html"}],
                "commonPattern": [{"ref": "pattern:demo"}],
                "governedBy": [{"ref": "ruling:s999-D1"}],
                "mustNotNeighbour": [{"ref": None, "$note": "legal declared prose"}],
            },
        }
        (components_dir / "Widget.meta.json").write_text(json.dumps(meta_a), encoding="utf-8")

        # --- meta B: deliberately BROKEN ref (dangling component:) ----
        meta_b = dict(meta_a)
        meta_b["name"] = "Broken"
        meta_b["edges"] = {"consumes": [{"ref": "component:does-not-exist", "$note": "bad"}]}
        (components_dir / "Broken.meta.json").write_text(json.dumps(meta_b), encoding="utf-8")

        # --- meta C: MISSING provenance -------------------------------
        meta_c = dict(meta_a)
        del meta_c["provenance"]
        meta_c["name"] = "NoProvenance"
        meta_c["edges"] = {}
        (components_dir / "NoProvenance.meta.json").write_text(json.dumps(meta_c), encoding="utf-8")

        fails_out, null_note_count, n_files = validate_corpus(
            components_dir=components_dir, proforma_dir=proforma_dir, snippets_dir=snippets_dir,
            nodes_pattern_path=nodes_pattern_path, nodes_context_path=nodes_context_path,
            rulings_path=rulings_path, schema_path=schema_path,
        )
        reasons = "\n".join(fails_out)

        bite("selftest corpus is isolated (3 metas seen, none from the live tree)", n_files == 3)
        bite("arm 1 — deliberately broken ref FAILS",
             any("Broken.meta.json" in f and "does not resolve" in f for f in fails_out))
        bite("arm 2 — legal ref:null + $note on meta A does not fail, and is counted",
             not any("Widget.meta.json" in f and "mustNotNeighbour" in f for f in fails_out)
             and null_note_count >= 1)
        bite("arm 2b — every OTHER legal ref on meta A resolves clean (renderedBy/commonPattern/governedBy)",
             not any("Widget.meta.json" in f for f in fails_out))
        bite("arm 3 — meta missing `provenance` FAILS",
             any("NoProvenance.meta.json" in f and "provenance" in f for f in fails_out))
        bite("selftest never touched the live corpus",
             not any(str(COMPONENTS) in f or str(PROFORMA_DIR) in f for f in fails_out))

    if fails:
        print(f"\nselftest FAILED — {len(fails)} bite(s): {fails}")
        return 1
    print("\nselftest OK.")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
