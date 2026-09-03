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

RESOLUTIONS INPUT (s135-D4, RULED #135 — enacted here):
  reviews/KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json is a GENERATOR INPUT,
  compiled in on EVERY rebuild. It is not a patch applied after the fact: the
  generator still wipes and rebuilds `edges` from scratch each run, but the
  ruled verdicts are folded into that rebuild, so Dave-ruled merges /
  promotions / attaches survive regeneration as machinery. Three shapes:
    MERGE   (nearmiss) — a context: node the verdicts fold into a component:
                         node. Applied at node-id level in the livesInside
                         loop, so the edge lands in containedBy (not
                         usedInContext) and the merged context node is NOT
                         registered in _nodes-context.json.
    PROMOTE (prose)    — a (meta filename, edge-type, $note) triple whose ref
                         the verdicts resolve to a component. Applied as a
                         post-pass over the freshly built edge set, so it
                         works for ANY edge type, including the five the
                         generator otherwise hard-codes to ref:null.
    ATTACH  (governed) — governedBy ruling attributions, per component stem.
  PRECEDENCE: the resolutions file WINS over the generator's own derivation.
  Every compiled resolution MUST land — an unlanded one is a LOUD, NAMED fail
  (a stale verdicts file must not silently no-op). A missing / unparseable /
  malformed resolutions file is a LOUD refusal, never a silent default.
  `_validate_kg.py` check (f) independently re-derives the same facts from the
  verdicts file and asserts them present in the live corpus.

NOT populated by this script (Dave's-eye batch per s133-D1 status line):
  governedBy BEYOND what the resolutions file rules, token-claim edges
  (separate lane), and any semantic dedup beyond case/whitespace-normalised
  string identity.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
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

# s135-D4 — the ruled verdicts file is a GENERATOR INPUT, not a hand-patch.
RESOLUTIONS = ROOT.parent / "reviews" / "KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json"

# The five edge types the generator otherwise hard-codes to ref:null. Listed
# for documentation only — the PROMOTE post-pass is deliberately generic and
# applies to any edge type the resolutions file names.
PROSE_EDGE_TYPES = ("mustNotNeighbour", "triggeredBy", "hasPart", "partial", "family")

EXCLUDE = {"EXAMPLE-button.meta.json"}


class ResolutionsError(RuntimeError):
    """Loud + named refusal. NEVER defaulted, never swallowed: a resolutions
    file that cannot be read is a build that would silently drop Dave-ruled
    verdicts, which is exactly the s135-D4 root cause."""


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


def load_resolutions(comp_idx, path=None):
    """(s135-D4) Read + COMPILE the ruled verdicts file into the three lookup
    tables the rebuild consumes. Every failure mode is loud and named."""
    path = path or RESOLUTIONS
    if not path.exists():
        raise ResolutionsError(
            f"RESOLUTIONS INPUT MISSING — {path}. s135-D4 requires this file be "
            f"compiled in on every rebuild; refusing to regenerate a corpus that "
            f"would silently drop every ruled verdict."
        )
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ResolutionsError(f"RESOLUTIONS INPUT UNPARSEABLE — {path}: {e!r}")
    if not isinstance(raw, dict):
        raise ResolutionsError(f"RESOLUTIONS INPUT MALFORMED — {path}: top level is not an object")
    for section in ("nearmiss", "prose", "governed"):
        if not isinstance(raw.get(section), list):
            raise ResolutionsError(
                f"RESOLUTIONS INPUT MALFORMED — {path}: section '{section}' is missing or not a list"
            )

    def resolve_component(name, where):
        node = comp_idx.get(norm(name)) or comp_idx.get(norm(name.replace("-", " ")))
        if not node:
            raise ResolutionsError(
                f"RESOLUTIONS INPUT UNRESOLVABLE — {path}: {where} names '{name}', "
                f"which matches no component meta stem"
            )
        return node

    merges, promotes, governed = {}, {}, {}
    rows = 0

    for r in raw["nearmiss"]:
        if r.get("verdict") != "MERGE":
            continue
        rows += 1
        node = r.get("node")
        cand = (r.get("cand") or "").split(",")[0].split("(")[0].strip()
        if not node or not cand:
            raise ResolutionsError(f"RESOLUTIONS INPUT MALFORMED — {path}: nearmiss MERGE row missing node/cand: {r!r}")
        target = resolve_component(cand, f"nearmiss MERGE row for {node}")
        if node in merges and merges[node] != target:
            raise ResolutionsError(f"RESOLUTIONS INPUT CONFLICT — {path}: {node} merged to two targets")
        merges[node] = target

    for r in raw["prose"]:
        verdict = r.get("verdict") or ""
        if not verdict.startswith("PROMOTE"):
            continue
        rows += 1
        name = verdict.split("→", 1)[1] if "→" in verdict else ""
        if not name.strip():
            raise ResolutionsError(f"RESOLUTIONS INPUT MALFORMED — {path}: prose PROMOTE row has no target: {r!r}")
        key = (r.get("file"), r.get("grp"), r.get("note"))
        if not all(key):
            raise ResolutionsError(f"RESOLUTIONS INPUT MALFORMED — {path}: prose row missing file/grp/note: {r!r}")
        target = resolve_component(name.strip(), f"prose PROMOTE row {key[0]}/{key[1]}")
        if key in promotes and promotes[key] != target:
            raise ResolutionsError(f"RESOLUTIONS INPUT CONFLICT — {path}: prose row {key} promoted to two targets")
        promotes[key] = target

    for r in raw["governed"]:
        if r.get("verdict") != "ATTACH":
            continue
        rows += 1
        comp, rid = r.get("comp"), r.get("rid")
        if not comp or not rid:
            raise ResolutionsError(f"RESOLUTIONS INPUT MALFORMED — {path}: governed ATTACH row missing comp/rid: {r!r}")
        resolve_component(comp, "governed ATTACH row")
        governed.setdefault(comp, [])
        if rid not in governed[comp]:
            governed[comp].append(rid)

    return {
        "path": path,
        "merges": merges,
        "promotes": promotes,
        "governed": {k: sorted(v) for k, v in governed.items()},
        "rows": rows,
        "landed": {"merge": {}, "promote": {}, "attach": {}},
    }


def apply_promotions(edges, fname, res):
    """PROMOTE post-pass. Deliberately generic across edge types: the ruled
    (file, edge-type, $note) triple WINS over whatever ref the generator's own
    derivation produced (including its hard-coded ref:null)."""
    n = 0
    for etype, arr in edges.items():
        for e in arr:
            key = (fname, etype, e.get("$note"))
            target = res["promotes"].get(key)
            if target is None:
                continue
            e["ref"] = target
            res["landed"]["promote"][key] = res["landed"]["promote"].get(key, 0) + 1
            n += 1
    return n


def build_edges_for_meta(data, stem, comp_idx, snip_idx, pattern_registry, context_registry, res, fname):
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
            merged = res["merges"].get(node_id)
            if merged:
                # s135-D4 MERGE: the verdicts fold this context node into a
                # component node. It becomes a containedBy edge and the
                # context node is NOT registered — the registry entry would
                # be an orphan of a node Dave ruled out of existence.
                contained.append({"ref": merged, "$note": target})
                res["landed"]["merge"][node_id] = res["landed"]["merge"].get(node_id, 0) + 1
                continue
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

    # s135-D4 PROMOTE — ruled refs win over the generator's own derivation.
    apply_promotions(edges, fname, res)

    # s135-D4 ATTACH — governedBy is emitted ONLY from the resolutions file.
    # Nothing here invents an attribution; anything beyond the ruled set stays
    # the Dave's-eye batch per s133-D1.
    rids = res["governed"].get(stem)
    if rids:
        edges["governedBy"] = [{"ref": f"ruling:{r}"} for r in rids]
        res["landed"]["attach"][stem] = sorted(rids)

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
    res = load_resolutions(comp_idx)

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

        edges = build_edges_for_meta(data_before, stem, comp_idx, snip_idx, pattern_registry, context_registry, res, f.name)

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

    # s135-D4 — every compiled resolution MUST have landed. A verdicts file
    # that has gone stale against the corpus must fail LOUD and NAMED, never
    # silently no-op (that silence is the defect this ruling exists to kill).
    unlanded = []
    for node in sorted(res["merges"]):
        if not res["landed"]["merge"].get(node):
            unlanded.append(f"MERGE {node} -> {res['merges'][node]} — no livesInside target generated that context node")
    for key in sorted(res["promotes"], key=lambda k: (k[0], k[1], k[2])):
        if not res["landed"]["promote"].get(key):
            unlanded.append(f"PROMOTE {key[0]} / {key[1]} / $note={key[2][:60]!r} — no matching edge in the rebuilt corpus")
    for stem_ in sorted(res["governed"]):
        if not res["landed"]["attach"].get(stem_):
            unlanded.append(f"ATTACH {stem_} — no meta with that stem was processed")
    if unlanded:
        print(f"RESOLUTIONS NOT LANDED — {res['path']} is stale against the corpus:", file=sys.stderr)
        for u in unlanded:
            print(f"  x {u}", file=sys.stderr)
        sys.exit(1)

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
    n_merge_edges = sum(res["landed"]["merge"].values())
    n_promote_edges = sum(res["landed"]["promote"].values())
    n_attach_edges = sum(len(v) for v in res["landed"]["attach"].values())
    print(
        f"resolutions consumed ({res['path'].name}): {res['rows']} ruled rows compiled -> "
        f"MERGE {len(res['merges'])} rules on {n_merge_edges} edges, "
        f"PROMOTE {len(res['promotes'])} keys on {n_promote_edges} edges, "
        f"ATTACH {n_attach_edges} governedBy edges across {len(res['landed']['attach'])} components"
    )


if __name__ == "__main__":
    try:
        main()
    except ResolutionsError as e:
        print(f"gen_kg_edges.py: REFUSED — {e}", file=sys.stderr)
        sys.exit(2)
