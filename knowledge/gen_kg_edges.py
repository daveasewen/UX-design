#!/usr/bin/env python3
"""
gen_kg_edges.py — mechanical KG edge migration for the component meta corpus.
Ruling: s131-D2 (RULED #131, NOT ENACTED) + s133-D1 (RULED #133, scope widened).
MECHANICAL batch only — see notes/_briefs/2026-08-08-133-... and the sub brief
that generated this file. By-addition: never deletes/overwrites existing meta
prose or fields. Idempotent / re-runnable: only (re)writes the top-level
`edges` field per file, byte-preserving everything else (insertion is a pure
text splice before the file's final closing brace, not a JSON re-serialize).

Populates (mechanical, resolvable-by-string-match only — no invention):
  renderedBy      -> knowledge/snippets/<Stem>.reference.html if it exists
  consumes/reuses -> component refs found by name-matching $consumes/$reuses
                     prose against the component stem registry; unresolved
                     mentions get ref:null + $note (flagged, not invented)
  hasPart         -> subComponents keys (ref:null always — these are internal
                     parts, not top-level nodes in the id grammar; $note holds
                     the part name + its 'use'/description)
  partial         -> $partials prose (ref:null + $note — free text, not a
                     structured list; Dave's-eye territory to convert)
  family          -> $family prose (ref:null + $note, same reasoning)
  containedBy     -> relationships.livesInside targets that name-match a
                     component stem
  usedInContext   -> relationships.livesInside targets that do NOT match a
                     component stem (context registry node)
  commonPattern   -> relationships.commonPatterns (pattern registry node)
  mustNotNeighbour, triggeredBy -> ref:null + $note (prose, awaiting Dave's-eye
                     pass per s131-D2/s133-D1 split; not invented as refs)

NOT populated by this script (Dave's-eye batch per s133-D1 status line):
  governedBy (ruling attributions), token-claim edges (separate lane), and any
  semantic dedup beyond case/whitespace-normalised string identity.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPONENTS = ROOT / "components"
PROFORMA = ROOT / "_proforma" / "icon-button.meta.json"
SNIPPETS = ROOT / "snippets"
NODES_PATTERN = COMPONENTS / "_nodes-pattern.json"
NODES_CONTEXT = COMPONENTS / "_nodes-context.json"

EXCLUDE = {"EXAMPLE-button.meta.json"}


def norm(s):
    """case/whitespace-normalised string identity — the only 'merge' this
    script is allowed to do per the DO-NOT-RULE list (nothing fuzzier)."""
    return re.sub(r"\s+", " ", s.strip().lower())


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.strip().lower())
    return re.sub(r"-+", "-", s).strip("-")


def collect_files():
    files = sorted(f for f in COMPONENTS.glob("*.meta.json") if f.name not in EXCLUDE)
    files.append(PROFORMA)
    return files


def component_stem_index(files):
    """norm(stem-with-spaces) -> 'component:<stem>' for name matching."""
    idx = {}
    for f in files:
        stem = f.stem.replace(".meta", "") if f.name != "icon-button.meta.json" or f.parent != PROFORMA.parent else f.stem.replace(".meta", "")
        stem = f.name[: -len(".meta.json")]
        key1 = norm(stem)
        key2 = norm(stem.replace("-", " "))
        node_id = f"component:{stem}"
        idx[key1] = node_id
        idx[key2] = node_id
    return idx


def snippet_index():
    """norm(stem) -> snippet filename, for renderedBy matching."""
    idx = {}
    if SNIPPETS.exists():
        for f in SNIPPETS.glob("*.reference.html"):
            stem = f.name[: -len(".reference.html")]
            idx[norm(stem)] = f.name
            idx[norm(stem.replace("-", " "))] = f.name
    return idx


def find_component_ref(text, comp_idx):
    """Look for any known component stem name mentioned inside a free-text
    string. Returns node-id or None. First match wins (deterministic scan
    order = longest stem first, to avoid short-name false positives)."""
    tl = " " + re.sub(r"[()\[\]/.,:;\"']", " ", text.lower()) + " "
    best = None
    best_len = 0
    for key, node_id in comp_idx.items():
        if len(key) < 3:
            continue
        pat = " " + key + " "
        if pat in tl or tl.startswith(key + " ") or tl.endswith(" " + key):
            if len(key) > best_len:
                best = node_id
                best_len = len(key)
    return best


def build_edges_for_meta(data, stem, comp_idx, snip_idx, pattern_registry, context_registry):
    edges = {}

    # renderedBy
    key = norm(stem)
    key2 = norm(stem.replace("-", " "))
    snip = snip_idx.get(key) or snip_idx.get(key2)
    if snip:
        edges["renderedBy"] = [{"ref": f"snippet:{snip}"}]

    rel = data.get("relationships", {}) or {}

    # containedBy / usedInContext from livesInside
    contained, used_ctx = [], []
    for target in rel.get("livesInside", []) or []:
        cref = find_component_ref(target, comp_idx) if len(target) < 40 else None
        # prefer exact/near-exact stem match over substring scan for short targets
        exact = comp_idx.get(norm(target)) or comp_idx.get(norm(target.replace("-", " ")))
        ref = exact or cref
        if ref:
            contained.append({"ref": ref, "$note": target})
        else:
            slug = slugify(target)
            node_id = f"context:{slug}"
            used_ctx.append({"ref": node_id, "$note": target})
            entry = context_registry.setdefault(node_id, {"id": node_id, "label": target, "sources": []})
            if stem not in entry["sources"]:
                entry["sources"].append(stem)
    if contained:
        edges["containedBy"] = contained
    if used_ctx:
        edges["usedInContext"] = used_ctx

    # commonPattern
    cps = []
    for p in rel.get("commonPatterns", []) or []:
        slug = slugify(p)
        node_id = f"pattern:{slug}"
        cps.append({"ref": node_id})
        entry = pattern_registry.setdefault(node_id, {"id": node_id, "label": p, "sources": []})
        if stem not in entry["sources"]:
            entry["sources"].append(stem)
    if cps:
        edges["commonPattern"] = cps

    # mustNotNeighbour / triggeredBy — prose, not invented as refs
    mnn = rel.get("mustNotNeighbour", []) or []
    if mnn:
        edges["mustNotNeighbour"] = [{"ref": None, "$note": x} for x in mnn]
    tb = rel.get("triggeredBy", []) or []
    if tb:
        edges["triggeredBy"] = [{"ref": None, "$note": x} for x in tb]

    # $consumes / $reuses — list of prose strings, name-match against components
    for src_key, out_key in (("$consumes", "consumes"), ("$reuses", "reuses")):
        vals = data.get(src_key)
        if not vals:
            continue
        if isinstance(vals, str):
            vals = [vals]
        out = []
        for v in vals:
            ref = find_component_ref(v, comp_idx)
            out.append({"ref": ref, "$note": v})
        if out:
            edges[out_key] = out

    # subComponents -> hasPart (internal parts are not top-level nodes; always ref:null)
    sc = data.get("subComponents")
    if sc:
        out = []
        if isinstance(sc, dict):
            for part_name, spec in sc.items():
                use = spec.get("use") if isinstance(spec, dict) else str(spec)
                note = f"{part_name}: {use}" if use else part_name
                out.append({"ref": None, "$note": note})
        elif isinstance(sc, list):
            for item in sc:
                out.append({"ref": None, "$note": json.dumps(item, ensure_ascii=False) if not isinstance(item, str) else item})
        if out:
            edges["hasPart"] = out

    # $partials — free prose, ref:null
    partials = data.get("$partials")
    if partials:
        edges["partial"] = [{"ref": None, "$note": partials if isinstance(partials, str) else json.dumps(partials, ensure_ascii=False)}]

    # $family — free prose, ref:null
    family = data.get("$family")
    if family:
        edges["family"] = [{"ref": None, "$note": family if isinstance(family, str) else json.dumps(family, ensure_ascii=False)}]

    return edges


def splice_edges(raw, edges):
    """Insert/replace the top-level `edges` key by pure text splice — never
    re-serialises the rest of the file, so non-edges content is byte-for-byte
    unchanged (round-trip requirement)."""
    stripped_end = len(raw.rstrip())
    assert raw[:stripped_end].rstrip()[-1:] == "}", "file does not end with a JSON object close"
    tail = raw[stripped_end:]  # trailing whitespace/newline after final }
    # find the position of the final top-level closing brace
    final_brace_idx = raw.rstrip().rfind("}")
    before = raw[:final_brace_idx]
    after = raw[final_brace_idx:]  # '}' + tail

    edges_json = json.dumps(edges, indent=2, ensure_ascii=False)
    lines = edges_json.split("\n")
    indented = lines[0] + "\n" + "\n".join("  " + l for l in lines[1:])

    before_stripped = before.rstrip()
    insertion = ',\n  "edges": ' + indented + "\n"
    new_raw = before_stripped + insertion + after
    return new_raw


def remove_existing_edges_field(raw):
    """Idempotency: if a previous run already added `edges`, strip it out of
    the raw text (by JSON-aware splice) before regenerating, so re-runs don't
    duplicate the key. Only touches the `edges` key; everything else is
    reconstructed from the parsed dict order via text splice, same as first run."""
    data = json.loads(raw)
    if "edges" not in data:
        return raw
    # Rebuild raw without edges: safest is to re-splice using a version of
    # the object serialisation minus edges — but since we must not touch
    # byte formatting of other fields, do a targeted regex-free structural
    # removal: reparse and re-run insertion logic against a raw string with
    # the edges block textually removed.
    idx = raw.find('"edges"')
    if idx == -1:
        return raw
    # walk backward to the preceding comma (or newline) that starts this entry
    start = raw.rfind(",", 0, idx)
    # walk forward from idx to find the matching closing brace of the edges object
    brace_start = raw.find("{", idx)
    depth = 0
    i = brace_start
    while i < len(raw):
        if raw[i] == "{":
            depth += 1
        elif raw[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    end = i + 1  # position after edges object's closing brace
    new_raw = raw[:start] + raw[end:]
    return new_raw


def main():
    files = collect_files()
    comp_idx = component_stem_index(files)
    snip_idx = snippet_index()

    pattern_registry = {}
    context_registry = {}

    counts = {}
    resolved = {"consumes": 0, "reuses": 0, "containedBy": 0}
    unresolved = {"consumes": 0, "reuses": 0, "containedBy": 0}

    for f in files:
        raw = f.read_text(encoding="utf-8")
        raw_clean = remove_existing_edges_field(raw)
        data_before = json.loads(raw_clean)
        stem = f.name[: -len(".meta.json")]

        edges = build_edges_for_meta(data_before, stem, comp_idx, snip_idx, pattern_registry, context_registry)

        for etype, arr in edges.items():
            counts[etype] = counts.get(etype, 0) + len(arr)
            if etype in resolved:
                for e in arr:
                    if e.get("ref"):
                        resolved[etype] += 1
                    else:
                        unresolved[etype] += 1

        new_raw = splice_edges(raw_clean, edges)

        # verify: parses, and non-edges content is unchanged from ORIGINAL file
        new_data = json.loads(new_raw)
        original_data = json.loads(raw)  # includes any prior edges field, for comparison baseline
        original_data.pop("edges", None)
        check_data = dict(new_data)
        check_data.pop("edges", None)
        if check_data != original_data:
            print(f"ROUND-TRIP MISMATCH on {f}", file=sys.stderr)
            sys.exit(1)

        f.write_text(new_raw, encoding="utf-8")

    # write registries (sorted for determinism)
    pattern_list = [pattern_registry[k] for k in sorted(pattern_registry)]
    context_list = [context_registry[k] for k in sorted(context_registry)]
    NODES_PATTERN.write_text(json.dumps(pattern_list, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    NODES_CONTEXT.write_text(json.dumps(context_list, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"files processed: {len(files)}")
    print(f"edge counts by type: {json.dumps(counts, indent=2)}")
    print(f"resolved vs ref:null (consumes/reuses/containedBy only): resolved={resolved} unresolved={unresolved}")
    print(f"pattern nodes: {len(pattern_list)}")
    print(f"context nodes: {len(context_list)}")


if __name__ == "__main__":
    main()
