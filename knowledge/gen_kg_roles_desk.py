#!/usr/bin/env python3
"""gen_kg_roles_desk.py — the ROLE / DESK-address edge generator (#270 lane 1).

Enacts s269-D1 order item 1: put ROLES and the DESK address fields into the
component KG. Four edge types, all component-sourced, all read from the METAS
(the ruled canon, s251-D12 / s254-D2 item 3) and resolved against the three
closed stores — never from knowledge/roles.json's own `providers` lists, which
are a MEMBERSHIP CROSS-CHECK and are measurably stale (see ROLES-DRIFT.md).

  providesRole    component -> role:<slug>     from meta `provides`
                                               resolved against knowledge/roles.json
  answersIntent   component -> intent:<word>   from meta `answers` (string or list)
                                               resolved against knowledge/chart-intents.json
  hasDataShape    component -> shape:<value>   from meta `shape`
                                               resolved against knowledge/shapes.json
  yieldsTo        component -> component       parsed from the PROSE half of meta `when`
                                               (s253-D1: the beats/yields sentence after the
                                               first em-dash), resolved against the meta stems

⛔ A NEW EDGE TYPE IS A CLOSED-VOCABULARY CHANGE (#75). This script PROPOSES;
Dave ratifies; only then does it land. `--dry-run` is the DEFAULT and writes one
JSON file into the lane folder and nothing else. `--land` REFUSES unless
`--ratified sNNN-DN` names a ruling id that exists in knowledge/_rulings.json.
That refusal is mutation-tested in --selftest (bite 6).

The landing splice is by ADDITION, in the style of gen_kg_edges.py
(splice_edges_in_place / splice_edges): the existing `edges` VALUE is replaced
in place by text splice, every prior edge type is carried byte-for-byte, and a
re-run is a no-op (idempotent — proved by --selftest bite 5).

NEVER INVENTED (fence 3, #261): a target that does not resolve to a measured
thing becomes {"ref": null, "$note": "<the prose>"} and is counted in
`unresolved`. Two such entries exist today, both anaphora in the `when` prose
("yields to it", "yields to both") — declared, never guessed.

Usage:
  python3 knowledge/gen_kg_roles_desk.py                     # dry run (default)
  python3 knowledge/gen_kg_roles_desk.py --out /tmp/x.json   # dry run, named output
  python3 knowledge/gen_kg_roles_desk.py --land --ratified s270-D1
  python3 knowledge/gen_kg_roles_desk.py --selftest
  python3 knowledge/gen_kg_roles_desk.py --corpus <dir>      # operate on a scratch copy

DO-NOT-RULE: this script never adds a role, an intent word or a shape value to a
store, never edits meta.schema.json, and never touches _nodes-*.json. Widening
those is Dave's ruling (s252-D1 / s254-D2 item 1 / chart-intents.json $description).
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
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMPONENTS = HERE / "components"
ROLES = HERE / "roles.json"
INTENTS = HERE / "chart-intents.json"
SHAPES = HERE / "shapes.json"
RULINGS = HERE / "_rulings.json"
LANE = ROOT / "notes" / "_lanes" / "270" / "roles-desk"
DEFAULT_OUT = LANE / "DRY-RUN.json"

EXCLUDE = {"EXAMPLE-button.meta.json"}

EDGE_TYPES = ("providesRole", "answersIntent", "hasDataShape", "yieldsTo")

# s253-D1: a `when` value is GATE — PROSE, split on the FIRST em-dash; only the
# prose half carries the beats/yields sentence. when-fields.json $grammar.
EM_DASH = "—"
YIELD_RX = re.compile(r"yields?\s+to\s+", re.I)
BEATS_RX = re.compile(r"\bbeats\s+", re.I)
NAME_RX = re.compile(r"([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)")
CONT_RX = re.compile(r"(?:,|\band)\s+to\s+([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)")
# Anaphora the prose uses instead of naming the sibling. NOT resolved — ref:null.
ANAPHORA = {"it", "both", "them", "either", "these", "those"}


# ------------------------------------------------------------------ corpus

def meta_files(components_dir=None):
    d = components_dir or COMPONENTS
    return sorted(f for f in d.glob("*.meta.json") if f.name not in EXCLUDE)


def load_store(path, key):
    """The store's address set. Loud on a missing file: a silently empty
    vocabulary would turn every edge into an unresolved null."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    vocab = data[key]
    return set(vocab.keys()) if isinstance(vocab, dict) else set(vocab)


def load_stores(roles=None, intents=None, shapes=None):
    return {
        "role": load_store(roles or ROLES, "roles"),
        "intent": load_store(intents or INTENTS, "chart-intent"),
        "shape": load_store(shapes or SHAPES, "shapes"),
    }


# ------------------------------------------------------------------ parsing

def prose_half(when):
    """The half after the FIRST em-dash. '' when the value is gate-only."""
    if not isinstance(when, str) or EM_DASH not in when:
        return ""
    return when.split(EM_DASH, 1)[1].strip()


def yield_candidates(prose):
    """Every name the prose declares this component YIELDS TO, in order.

    Segments the prose at the `yields to` / `beats` verbs and reads only the
    yields segments: the first name after the verb, plus every `, to X` /
    `and to X` continuation inside the same segment. `beats` is the inverse
    claim and is deliberately NOT turned into an edge here — an edge lives on
    the meta that declares it, and 'X beats Y' is Y's fact, not X's.
    """
    marks = [(m.start(), m.end(), "Y") for m in YIELD_RX.finditer(prose)]
    marks += [(m.start(), m.end(), "B") for m in BEATS_RX.finditer(prose)]
    marks.sort()
    out = []
    for i, (_s, e, kind) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(prose)
        seg = prose[e:end]
        if kind != "Y":
            continue
        names = []
        m0 = NAME_RX.match(seg.lstrip())
        if m0:
            names.append(m0.group(1))
        names += [m.group(1) for m in CONT_RX.finditer(seg)]
        for n in names:
            out.append((n, seg.strip()))
    return out


# ------------------------------------------------------------------ derive

def build(components_dir=None, stores=None):
    """Returns (per_file_edges, report). per_file_edges: {filename: {etype: [edge]}}."""
    files = meta_files(components_dir)
    stores = stores or load_stores()
    stems = {f.name[: -len(".meta.json")] for f in files}
    by_lower = {s.lower(): s for s in stems}

    per_file = {}
    evidence = []
    unresolved = []
    nodes = {"role": set(), "intent": set(), "shape": set()}

    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        stem = f.name[: -len(".meta.json")]
        edges = {}

        # providesRole
        prov = data.get("provides")
        if isinstance(prov, str) and prov:
            ok = prov in stores["role"]
            ref = f"role:{prov}" if ok else None
            edges.setdefault("providesRole", []).append(
                {"ref": ref} if ok else {"ref": None, "$note": f"provides: {prov} — no such role in roles.json"}
            )
            if ok:
                nodes["role"].add(ref)
            else:
                unresolved.append({"file": f.name, "type": "providesRole", "value": prov,
                                   "why": "not a key of knowledge/roles.json roles"})
            evidence.append({"component": stem, "type": "providesRole", "ref": ref,
                             "file": f"knowledge/components/{f.name}", "field": "provides", "value": prov})

        # answersIntent
        ans = data.get("answers")
        if ans:
            for word in (ans if isinstance(ans, list) else [ans]):
                ok = word in stores["intent"]
                ref = f"intent:{word}" if ok else None
                edges.setdefault("answersIntent", []).append(
                    {"ref": ref} if ok else {"ref": None, "$note": f"answers: {word} — no such word in chart-intents.json"}
                )
                if ok:
                    nodes["intent"].add(ref)
                else:
                    unresolved.append({"file": f.name, "type": "answersIntent", "value": word,
                                       "why": "not a key of knowledge/chart-intents.json chart-intent"})
                evidence.append({"component": stem, "type": "answersIntent", "ref": ref,
                                 "file": f"knowledge/components/{f.name}", "field": "answers", "value": word})

        # hasDataShape
        shp = data.get("shape")
        if isinstance(shp, str) and shp:
            ok = shp in stores["shape"]
            ref = f"shape:{shp}" if ok else None
            edges.setdefault("hasDataShape", []).append(
                {"ref": ref} if ok else {"ref": None, "$note": f"shape: {shp} — no such value in shapes.json"}
            )
            if ok:
                nodes["shape"].add(ref)
            else:
                unresolved.append({"file": f.name, "type": "hasDataShape", "value": shp,
                                   "why": "not a key of knowledge/shapes.json shapes"})
            evidence.append({"component": stem, "type": "hasDataShape", "ref": ref,
                             "file": f"knowledge/components/{f.name}", "field": "shape", "value": shp})

        # yieldsTo
        prose = prose_half(data.get("when"))
        seen = set()
        for name, seg in yield_candidates(prose):
            low = name.lower()
            if low in ANAPHORA:
                note = f"`when` prose yields to \"{name}\" — anaphoric, the sibling is not named: {seg[:160]}"
                edges.setdefault("yieldsTo", []).append({"ref": None, "$note": note})
                unresolved.append({"file": f.name, "type": "yieldsTo", "value": name,
                                   "why": "anaphora in the `when` prose — target not named, never guessed"})
                evidence.append({"component": stem, "type": "yieldsTo", "ref": None,
                                 "file": f"knowledge/components/{f.name}", "field": "when", "value": seg[:200]})
                continue
            target = by_lower.get(low)
            if not target or target == stem or f"component:{target}" in seen:
                continue
            seen.add(f"component:{target}")
            edges.setdefault("yieldsTo", []).append({"ref": f"component:{target}"})
            evidence.append({"component": stem, "type": "yieldsTo", "ref": f"component:{target}",
                             "file": f"knowledge/components/{f.name}", "field": "when", "value": seg[:200]})

        if edges:
            per_file[f.name] = edges

    counts = {t: sum(len(e.get(t, [])) for e in per_file.values()) for t in EDGE_TYPES}
    report = {
        "generated_by": "knowledge/gen_kg_roles_desk.py",
        "corpus": str(components_dir or COMPONENTS),
        "metas_read": len(files),
        "metas_carrying_new_edges": len(per_file),
        "edge_counts": counts,
        "edge_total": sum(counts.values()),
        "node_counts": {k: len(v) for k, v in nodes.items()},
        "nodes": {k: sorted(v) for k, v in nodes.items()},
        "store_vocabulary_sizes": {k: len(v) for k, v in stores.items()},
        "unresolved": unresolved,
        "evidence": evidence,
    }
    return per_file, report


# ------------------------------------------------------------------ splice

def edges_block_span(raw):
    """(start, end) of the top-level `edges` object VALUE in raw text, or None.
    Same walk as gen_kg_edges.py:_edges_block_span — string-aware, so a brace
    inside a $note does not end the block."""
    idx = raw.find('"edges"')
    if idx == -1:
        return None
    brace_start = raw.find("{", idx)
    if brace_start == -1:
        return None
    depth, i, in_str, esc = 0, brace_start, False, False
    while i < len(raw):
        ch = raw[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return (brace_start, i + 1)
        i += 1
    return None


def _indented(edges):
    j = json.dumps(edges, indent=2, ensure_ascii=False).split("\n")
    return j[0] + "\n" + "\n".join("  " + l for l in j[1:])


def splice(raw, new_edges):
    """By addition: merge new_edges into the meta's existing `edges` and splice
    the block back where it already sits (or append the key if absent).
    Existing edge types are untouched; a new type already present is REPLACED by
    the derived list (which is what makes a re-run idempotent)."""
    data = json.loads(raw)
    prior = data.get("edges") or {}
    merged = {k: v for k, v in prior.items()}
    for etype in EDGE_TYPES:
        if etype in new_edges:
            merged[etype] = new_edges[etype]
    span = edges_block_span(raw)
    if span is not None:
        out = raw[: span[0]] + _indented(merged) + raw[span[1]:]
    else:
        stripped = raw.rstrip()
        final = stripped.rfind("}")
        out = stripped[:final].rstrip() + ',\n  "edges": ' + _indented(merged) + "\n" + stripped[final:] + raw[len(stripped):]
    # round-trip: nothing but `edges` may change
    before = json.loads(raw); before.pop("edges", None)
    after = json.loads(out); after.pop("edges", None)
    if before != after:
        raise RuntimeError("ROUND-TRIP MISMATCH — the splice changed non-edges content")
    return out


# ------------------------------------------------------------------ ratify

def ruling_exists(rid, rulings_path=None):
    p = Path(rulings_path or RULINGS)
    if not p.exists():
        return False
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ("rulings", "_README"):
        for entry in data.get(key, []) or []:
            if isinstance(entry, dict) and entry.get("id") == rid:
                return True
    return False


def land(components_dir=None, rulings_path=None, ratified=None, stores=None):
    """Refuses without a ratification id that EXISTS in _rulings.json (#75)."""
    if not ratified:
        raise SystemExit("REFUSED — --land needs --ratified sNNN-DN (a new edge type is a "
                         "closed-vocabulary change, #75: Dave ratifies, then it lands)")
    if not re.match(r"^s\d{2,4}-D\d+$", ratified):
        raise SystemExit(f"REFUSED — --ratified '{ratified}' is not a ruling id (sNNN-DN)")
    if not ruling_exists(ratified, rulings_path):
        raise SystemExit(f"REFUSED — ruling '{ratified}' is not in {rulings_path or RULINGS}. "
                         "An unrecorded ratification is not a ratification.")
    per_file, report = build(components_dir, stores)
    d = components_dir or COMPONENTS
    written = 0
    for name, edges in per_file.items():
        f = d / name
        raw = f.read_text(encoding="utf-8")
        out = splice(raw, edges)
        if out != raw:
            f.write_text(out, encoding="utf-8")
            written += 1
    report["landed"] = {"ratified": ratified, "files_written": written}
    return report


# ------------------------------------------------------------------ selftest

def _mini_corpus(tmp):
    """Synthetic corpus — touches nothing in the live tree."""
    c = tmp / "components"; c.mkdir(parents=True)
    (c / "alpha.meta.json").write_text(json.dumps({
        "name": "Alpha", "provenance": {"source": "code"},
        "provides": "headline-metric", "answers": "one-number",
        "shape": "one-measure × value-and-delta",
        "when": "shape = one-measure × value-and-delta — the default; beats beta when x; "
                "yields to beta (12, \"n\") when y, and to gamma (3) when z.",
        "edges": {"renderedBy": [{"ref": "snippet:Alpha.reference.html"}]},
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (c / "beta.meta.json").write_text(json.dumps({
        "name": "Beta", "provenance": {"source": "code"},
        "provides": "not-a-role", "answers": ["one-number", "not-a-word"],
        "shape": "no-such-shape",
        "when": "a — yields to it when q.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (c / "gamma.meta.json").write_text(json.dumps({
        "name": "Gamma", "provenance": {"source": "code"},
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return c


def selftest():
    stores = {"role": {"headline-metric"}, "intent": {"one-number"},
              "shape": {"one-measure × value-and-delta"}}
    fails = []

    def bite(n, desc, cond):
        print(("  ok  " if cond else "  FAIL") + f"  bite {n}: {desc}")
        if not cond:
            fails.append(n)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        c = _mini_corpus(tmp)
        per_file, rep = build(c, stores)

        # 1 — the four types derive from the four fields
        a = per_file["alpha.meta.json"]
        bite(1, "alpha derives providesRole/answersIntent/hasDataShape/yieldsTo",
             a.get("providesRole") == [{"ref": "role:headline-metric"}]
             and a.get("answersIntent") == [{"ref": "intent:one-number"}]
             and a.get("hasDataShape") == [{"ref": "shape:one-measure × value-and-delta"}]
             and [e["ref"] for e in a.get("yieldsTo", [])] == ["component:beta", "component:gamma"])

        # 2 — `beats` is NOT an edge (it is the sibling's fact, not this meta's)
        bite(2, "`beats beta` produces no yieldsTo beyond the two yields targets",
             len(a.get("yieldsTo", [])) == 2)

        # 3 — an unresolvable store value becomes ref:null + $note, never invented
        b = per_file["beta.meta.json"]
        bite(3, "off-vocabulary provides/answers/shape -> ref:null + $note",
             b["providesRole"][0]["ref"] is None and "$note" in b["providesRole"][0]
             and [e["ref"] for e in b["answersIntent"]] == ["intent:one-number", None]
             and b["hasDataShape"][0]["ref"] is None
             and len(rep["unresolved"]) == 4)

        # 4 — anaphora is declared, never guessed; a meta with no DESK fields gets nothing
        bite(4, "`yields to it` -> ref:null + $note; gamma carries no new edges",
             b["yieldsTo"] == [b["yieldsTo"][0]] and b["yieldsTo"][0]["ref"] is None
             and "gamma.meta.json" not in per_file)

        # 5 — land is by addition and idempotent
        land(c, RULINGS, "s269-D10", stores)
        raw1 = (c / "alpha.meta.json").read_text(encoding="utf-8")
        kept = json.loads(raw1)["edges"].get("renderedBy") == [{"ref": "snippet:Alpha.reference.html"}]
        land(c, RULINGS, "s269-D10", stores)
        raw2 = (c / "alpha.meta.json").read_text(encoding="utf-8")
        bite(5, "--land is by addition (renderedBy survives) and byte-idempotent",
             kept and raw1 == raw2 and json.loads(raw2)["edges"]["providesRole"] == [{"ref": "role:headline-metric"}])

        # 6 — MUTATION: --land refuses without a ratification that exists
        with tempfile.TemporaryDirectory() as td2:
            c2 = _mini_corpus(Path(td2))
            before = (c2 / "alpha.meta.json").read_text(encoding="utf-8")
            refusals = 0
            for bad in (None, "s999-D9", "not-a-ruling"):
                try:
                    land(c2, RULINGS, bad, stores)
                except SystemExit:
                    refusals += 1
            after = (c2 / "alpha.meta.json").read_text(encoding="utf-8")
            bite(6, "--land REFUSES with no id, an absent id and a malformed id, and writes nothing",
                 refusals == 3 and before == after)

        # 7 — the store vocabulary is read, never widened
        bite(7, "no store file is written by a dry run or a land",
             not any(p.name in ("roles.json", "chart-intents.json", "shapes.json")
                     for p in tmp.rglob("*.json")))

        # 8 — dry run writes exactly one file, and not into the corpus
        with tempfile.TemporaryDirectory() as td3:
            out = Path(td3) / "DRY.json"
            c3 = _mini_corpus(Path(td3) / "corp")
            snap = {p.name: p.read_text(encoding="utf-8") for p in c3.glob("*.json")}
            _dry(c3, out, stores)
            bite(8, "--dry-run writes its JSON and leaves every meta byte-identical",
                 out.exists() and all(p.read_text(encoding="utf-8") == snap[p.name] for p in c3.glob("*.json")))

    print(("SELFTEST PASS" if not fails else f"SELFTEST FAIL — bites {fails}"))
    return 1 if fails else 0


# ------------------------------------------------------------------ entry

def _dry(components_dir, out_path, stores=None):
    per_file, report = build(components_dir, stores)
    report["mode"] = "dry-run"
    report["proposed_edges_by_file"] = per_file
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main():
    try:  # #269 PARKED-WITH-A-TRIPWIRE hook: advisory print, never a gate
        import _parked; _parked.notice("kg-edge-gen")
    except BaseException:
        pass
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()

    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default

    corpus = Path(opt("--corpus")) if opt("--corpus") else None

    if "--land" in argv:
        rep = land(corpus, None, opt("--ratified"))
        print(f"LANDED — ratified {rep['landed']['ratified']} · {rep['landed']['files_written']} metas written · "
              f"{rep['edge_total']} edges ({rep['edge_counts']})")
        return 0

    out = Path(opt("--out", str(DEFAULT_OUT)))
    rep = _dry(corpus, out)
    print(f"DRY RUN — {rep['metas_read']} metas read · {rep['metas_carrying_new_edges']} would carry new edges")
    print(f"  edges: {rep['edge_total']}  {rep['edge_counts']}")
    print(f"  nodes: {rep['node_counts']}  unresolved: {len(rep['unresolved'])}")
    print(f"  wrote {out}")
    print("  NOT LANDED — a new edge type is a closed-vocabulary change (#75); --land needs --ratified sNNN-DN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
