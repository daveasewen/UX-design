#!/usr/bin/env python3
"""
_validate_polarities.py — THE POLARITY GATE (s238-D7): five refusals in the build and at the
commit seam, a derivation of the polarity status / edges / defaults declaration, and the ONLY
sanctioned writer for the polarity home.

THE HOME (s238-D1, declared #238-P — the P1 plan names no path, so it is `knowledge/brain/`):
  knowledge/brain/principles.json   the R1 register, seeded byte-for-byte (grades A/B/C/D/L; the
                                    s237-D1 names are DERIVED here, never re-typed there)
  knowledge/brain/polarities.json   the 30 polarity nodes — N typed parties, typed out-links
  knowledge/brain/stubs.json        declared stubs: a party that is a phrase, not a register node
  knowledge/brain/schema/polarity.schema.json   the consumer's grammar — READ by this gate
  knowledge/brain/_generated/       polarity-status.json · polarity-edges.json ·
                                    defaults-declaration.txt — GENERATED, content-fresh-checked

THE FIVE REFUSALS (s238-D7), each LOUD, NAMED, rc != 0, NOTHING WRITTEN:
  R1  a party or link ref that does not resolve against the live registers
      (R1-DANGLING · R1-SUPERSEDED · R1-SELF-PARTY · R1-CIRCULAR · R1-WRONG-REGISTER ·
       R1-UNDECLARED-STUB)
  R2  an untyped link (R2-UNTYPED · R2-UNKNOWN-TYPE — a fifth type is NOT ruled, refused)
  R3  a judgement text field of any name on a node — the only judgement is a typed link to a
      knowledge/_rulings.json id (R3-JUDGEMENT-FIELD · R3-QUOTE-TOO-LONG · R3-NOTE-TOO-LONG)
  R4  an authored edge file — pairwise edges exist only under _generated/ with a content-
      freshness check (R4-AUTHORED-GENERATED · R4-AUTHORED-EDGES · R4-STRAY-FILE)
  R5  a typed status (R5-TYPED-STATUS) — status is DERIVED with a clock (s238-D3, s237-D9)
Plus the schema refusals the same grammar implies (S-PARSE · S-SHAPE · S-ID · S-MIN-PARTIES ·
S-ROLE · S-DUP-ID · S-DUP-PARTY · S-STUB-SHAPE · S-DUP-STUB) and the freshness verdicts
(MISSING-GENERATED · STALE-GENERATED, remedy: --write).

DERIVED, WITH A CLOCK (s238-D3): every generated file carries `generated_at` and a
`content_sha256` over its body. `--check` re-derives with the ON-DISK clock and compares BYTES
(never mtime — the `index_freshness_check` discipline); a file lacking the header or failing its
own sha was HAND-WRITTEN and is refused as R4, which is a different verdict from STALE.
The status rules are a port of 237-T's `_derive_sort.py` (R-OBLIGATION first, then R-RESOLVED,
then R-OPEN); the open rows' RULE K / RULE D fields are COPIED from 237-T's open-tensions.json
and stay FLOATED. The `Defaults used:` declaration follows s238-D5: declared ONLY when a default
bent away from the conservative side; the T asset carries no per-row conservative marker, so the
rule is printed and every row is UNPROVEN (nothing is declared).

THE WRITER (`--add-polarity FILE` / `--add-stub FILE`) is TEXTUAL and PROVEN BY RECONSTRUCTION,
as `_inscribe_ruling.py` does: removing the inserted span must give back the original bytes,
the result must parse to exactly one more entry equal to the one submitted, and the whole gate
must pass on the resulting text BEFORE a byte is written. A refusal leaves every file untouched.

CONSUMERS (a gate without a consumer is not a gate — s238-D7's last sentence):
  knowledge/_build_all.py STEPS      `--check` (GATE) and `--selftest` (ABORT), appended
  knowledge/_git_commit.sh           `--check` before staging (POLARITY_ACK declares a gap)
  knowledge/_test_git_commit.py      the seam harness stubs + drives this gate's line

Usage:
  python3 knowledge/_validate_polarities.py --check                 # the gate (build + commit seam)
  python3 knowledge/_validate_polarities.py --write                 # refusals, then (re)generate
  python3 knowledge/_validate_polarities.py --selftest              # control + every refusal arm,
                                                                    #   on a copy of the REAL rows
  python3 knowledge/_validate_polarities.py --add-polarity e.json --dry-run|--write
  python3 knowledge/_validate_polarities.py --add-stub s.json --dry-run|--write
  ... --brain DIR   (or env POLARITY_BRAIN_DIR)  point at another home (fixtures, selftest)
Exit: 0 pass · 1 refusal/failure · 2 argv · 77 COULD-NOT-ASK (an input outside this tree).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

import _could_not_ask as cna  # noqa: E402 - after the help gate's path insert

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_BRAIN = os.path.join(HERE, "brain")
RULINGS = os.path.join(HERE, "_rulings.json")
OPEN_DEFAULTS_REL = "notes/_subreports/assets/2026-09-02-237-T-tensions-schema/open-tensions.json"
OPEN_DEFAULTS = os.path.join(REPO, OPEN_DEFAULTS_REL)
T_SORT_FIGURE = ("6 · 3 · 21", "notes/_subreports/assets/2026-09-02-237-T-tensions-schema/tension-sort.json")

HOME_FILES = ("principles.json", "polarities.json", "stubs.json")
SCHEMA_REL = os.path.join("schema", "polarity.schema.json")
GEN_DIR = "_generated"
GEN_FILES = ("polarity-status.json", "polarity-edges.json", "defaults-declaration.txt")
GEN_HEADER = "GENERATED — do not hand-edit (knowledge/_validate_polarities.py --write)"
ALLOWED_TOP = set(HOME_FILES) | {"schema", GEN_DIR}

# s237-D1 — the five grade names. DERIVED from the ruling id quoted here; principles.json keeps
# the R1 letters and is never re-typed (s234-D1: generation chain, never copy chain).
GRADE_NAMES = {"A": "REPLICATED", "B": "STUDIED", "C": "PRACTISED", "D": "DEBUNKED", "L": "OBLIGATION"}
OBLIGATION_GRADE = "L"

STUB_ID = re.compile(r"^st-[a-z0-9]+(?:-[a-z0-9]+)*$")
ASCII_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
POLARITY_ID = re.compile(r"^pl-[0-9]{2,}$")
SCHEMA_KEYWORDS = {"$schema", "$id", "title", "description", "type", "additionalProperties",
                   "required", "properties", "items", "enum", "pattern", "minItems", "minLength",
                   "maxWords", "x-refusals", "x-vocabulary"}


class Refused(Exception):
    """⚠ LOUD AND NAMED. `.name` is the refusal's name; `.detail` says where and what."""

    def __init__(self, name, detail):
        super().__init__(f"{name} — {detail}")
        self.name, self.detail = name, detail


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(s):
    return sha256_bytes(s.encode("utf-8"))


def words(s):
    return len(str(s).split())


def now_clock():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ============================================================================================
# LOADING — parse in the consumer's grammar (JSON), every failure NAMED
# ============================================================================================
def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_json(text, what):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise Refused("S-PARSE", f"{what} does not parse as JSON: {e}")


def load_home(brain, overrides=None):
    """Texts + parsed objects of the three home files, the schema and the rulings store.
    `overrides` maps a home filename to replacement TEXT (the writer validates in memory)."""
    overrides = overrides or {}
    home = {"brain": brain, "text": {}, "obj": {}}
    for name in HOME_FILES:
        path = os.path.join(brain, name)
        if name in overrides:
            text = overrides[name]
        elif os.path.exists(path):
            text = read_text(path)
        else:
            raise Refused("S-SHAPE", f"{name} is absent from the home {brain}")
        home["text"][name] = text
        home["obj"][name] = parse_json(text, name)
    schema_path = os.path.join(brain, SCHEMA_REL)
    if not os.path.exists(schema_path):
        raise Refused("S-SHAPE", f"schema absent: {schema_path}")
    home["schema"] = parse_json(read_text(schema_path), "polarity.schema.json")
    if not os.path.exists(RULINGS):
        raise Refused("S-SHAPE", f"knowledge/_rulings.json absent at {RULINGS}")
    rulings = parse_json(read_text(RULINGS), "_rulings.json")
    if not isinstance(rulings, dict) or not isinstance(rulings.get("rulings"), list):
        raise Refused("S-SHAPE", "_rulings.json has no `rulings` list")
    home["rulings"] = {}
    for r in rulings["rulings"]:
        if isinstance(r, dict) and isinstance(r.get("id"), str):
            home["rulings"][r["id"]] = r
    return home


# ============================================================================================
# THE SCHEMA — a small reader of draft-2020-12 core + the house `maxWords`. It REFUSES a
# keyword it does not implement, so a schema edit can never be silently half-enforced.
# ============================================================================================
def schema_keywords_supported(schema, path="schema"):
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k not in SCHEMA_KEYWORDS and path.split(".")[-1] != "properties":
                raise Refused("SCHEMA-KEYWORD-UNSUPPORTED",
                              f"{path}.{k}: this gate does not implement that keyword — implement "
                              f"it or remove it; an ignored keyword is an unenforced rule")
            if k in ("properties",):
                for pk, pv in v.items():
                    schema_keywords_supported(pv, f"{path}.properties.{pk}")
            elif k == "items":
                schema_keywords_supported(v, f"{path}.items")


def schema_validate(inst, schema, path, out):
    """Append (keyword, path, detail) for every violation. Pure."""
    t = schema.get("type")
    if t == "object":
        if not isinstance(inst, dict):
            out.append(("type", path, f"expected object, got {type(inst).__name__}"))
            return
        props = schema.get("properties", {})
        for r in schema.get("required", []):
            if r not in inst:
                out.append(("required", f"{path}.{r}", f"required key {r!r} is missing"))
        if schema.get("additionalProperties") is False:
            for k in inst:
                if k not in props:
                    out.append(("additionalProperties", f"{path}.{k}",
                                f"key {k!r} is not in the schema (allowed: {sorted(props)})"))
        for k, v in inst.items():
            if k in props:
                schema_validate(v, props[k], f"{path}.{k}", out)
    elif t == "array":
        if not isinstance(inst, list):
            out.append(("type", path, f"expected array, got {type(inst).__name__}"))
            return
        if "minItems" in schema and len(inst) < schema["minItems"]:
            out.append(("minItems", path, f"{len(inst)} item(s), minimum {schema['minItems']}"))
        if "items" in schema:
            for i, v in enumerate(inst):
                schema_validate(v, schema["items"], f"{path}[{i}]", out)
    elif t == "string":
        if not isinstance(inst, str):
            out.append(("type", path, f"expected string, got {type(inst).__name__}"))
            return
        if "enum" in schema and inst not in schema["enum"]:
            out.append(("enum", path, f"{inst!r} is not one of {schema['enum']}"))
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            out.append(("pattern", path, f"{inst!r} does not match {schema['pattern']}"))
        if "minLength" in schema and len(inst) < schema["minLength"]:
            out.append(("minLength", path, f"shorter than {schema['minLength']}"))
        if "maxWords" in schema and words(inst) > schema["maxWords"]:
            out.append(("maxWords", path, f"{words(inst)} words, maximum {schema['maxWords']}"))
    elif t is not None:
        out.append(("type", path, f"schema type {t!r} is not one this gate reads"))


def name_violation(kw, path, detail):
    """Map a schema violation to the refusal NAME s238-D7 / the schema's x-refusals promise."""
    leaf = path.rsplit(".", 1)[-1]
    if kw == "additionalProperties":
        if "status" in leaf.lower():
            return "R5-TYPED-STATUS"
        return "R3-JUDGEMENT-FIELD"
    if kw == "required" and leaf == "type" and ".links[" in path:
        return "R2-UNTYPED"
    if kw == "enum" and leaf == "type" and ".links[" in path:
        return "R2-UNKNOWN-TYPE"
    if kw == "maxWords" and leaf == "quote":
        return "R3-QUOTE-TOO-LONG"
    if kw == "maxWords" and leaf == "note":
        return "R3-NOTE-TOO-LONG"
    if kw == "pattern" and leaf == "ref":
        return "S-ID"
    if kw == "pattern" and leaf == "id":
        return "S-ID"
    if kw == "minItems" and leaf == "parties":
        return "S-MIN-PARTIES"
    if kw == "enum" and leaf == "role":
        return "S-ROLE"
    return "S-SCHEMA"


# ============================================================================================
# THE REFUSALS
# ============================================================================================
def check_home_dir(brain):
    """R4 — the home is a CLOSED directory: three homes, the schema, the generated dir.
    Any other file is a second stored shape (s238-D1) or an authored edge list."""
    fails = []
    if not os.path.isdir(brain):
        raise Refused("S-SHAPE", f"home directory absent: {brain}")
    for name in sorted(os.listdir(brain)):
        if name.startswith(".") or name == "__pycache__":
            continue
        if name in ALLOWED_TOP:
            continue
        path = os.path.join(brain, name)
        if name.endswith(".json") and os.path.isfile(path):
            try:
                obj = json.loads(read_text(path))
            except Exception:
                obj = None
            if isinstance(obj, dict) and any(k.lower().endswith("edges") for k in obj):
                fails.append(("R4-AUTHORED-EDGES",
                              f"{name} carries an `edges` key outside {GEN_DIR}/ — pairwise edges "
                              f"are DERIVED (s238-D1); delete it and run --write"))
                continue
        fails.append(("R4-STRAY-FILE",
                      f"{name} is not one of the homes ({', '.join(HOME_FILES)}), schema/ or "
                      f"{GEN_DIR}/ — a second stored shape for the same concept is refused (s238-D1)"))
    # the generated dir is CLOSED too: a hand-written file sitting beside the three derived ones
    # would wear the generated path's authority (refusal 4) without ever being derived
    gen_dir = os.path.join(brain, GEN_DIR)
    if os.path.isdir(gen_dir):
        for name in sorted(os.listdir(gen_dir)):
            if name.startswith(".") or name in GEN_FILES:
                continue
            fails.append(("R4-STRAY-FILE",
                          f"{GEN_DIR}/{name} is not one of the derived files ({', '.join(GEN_FILES)}) — "
                          f"nothing under the generated path may be authored (s238-D7 refusal 4)"))
    return fails


def check_stubs(stubs_obj):
    fails = []
    if not isinstance(stubs_obj, dict) or not isinstance(stubs_obj.get("stubs"), list):
        return [("S-SHAPE", "stubs.json must be an object with a `stubs` list")]
    seen_ids, seen_phrases = set(), set()
    for i, s in enumerate(stubs_obj["stubs"]):
        where = f"stubs[{i}]"
        if not isinstance(s, dict) or set(s) != {"id", "phrase"}:
            fails.append(("S-STUB-SHAPE", f"{where}: a stub is EXACTLY {{id, phrase}} and nothing "
                                          f"else (got {sorted(s) if isinstance(s, dict) else type(s).__name__})"))
            continue
        if not isinstance(s["id"], str) or not STUB_ID.match(s["id"]):
            fails.append(("S-STUB-SHAPE", f"{where}: id {s['id']!r} must match {STUB_ID.pattern}"))
        if not isinstance(s["phrase"], str) or not s["phrase"].strip():
            fails.append(("S-STUB-SHAPE", f"{where}: phrase must be a non-empty string"))
        elif words(s["phrase"]) > 15:
            fails.append(("R3-JUDGEMENT-FIELD", f"{where}: phrase is {words(s['phrase'])} words — a "
                                                f"stub is a phrase, not a paragraph (max 15)"))
        if s.get("id") in seen_ids:
            fails.append(("S-DUP-STUB", f"{where}: duplicate stub id {s['id']!r}"))
        if s.get("phrase") in seen_phrases:
            fails.append(("S-DUP-STUB", f"{where}: duplicate stub phrase {s['phrase']!r}"))
        seen_ids.add(s.get("id"))
        seen_phrases.add(s.get("phrase"))
    return fails


def check_principles(pr_obj):
    if not isinstance(pr_obj, dict) or not isinstance(pr_obj.get("principles"), list):
        return [("S-SHAPE", "principles.json must be an object with a `principles` list")], {}
    fails, reg = [], {}
    for i, p in enumerate(pr_obj["principles"]):
        if not isinstance(p, dict) or not isinstance(p.get("id"), str):
            fails.append(("S-SHAPE", f"principles[{i}] has no string id"))
            continue
        if p["id"] in reg:
            fails.append(("S-DUP-ID", f"principles.json: duplicate id {p['id']!r}"))
        if p.get("grade") not in GRADE_NAMES:
            fails.append(("S-SHAPE", f"principles[{i}] {p['id']}: grade {p.get('grade')!r} is not "
                                     f"one of {sorted(GRADE_NAMES)} (s237-D1)"))
        reg[p["id"]] = p
    return fails, reg


def check_polarities(home):
    """R1 · R2 · R3 · R5 and the schema refusals over polarities.json. Returns (fails, resolved)
    where resolved[pl-id] = list of party dicts with a DERIVED `kind` (+ `grade`)."""
    fails = []
    pol = home["obj"]["polarities.json"]
    schema = home["schema"]
    schema_keywords_supported(schema)
    if not isinstance(pol, dict) or not isinstance(pol.get("polarities"), list):
        return [("S-SHAPE", "polarities.json must be an object with a `polarities` list")], {}
    for k in pol:
        if k not in ("$description", "$migration", "polarities"):
            fails.append(("R3-JUDGEMENT-FIELD", f"polarities.json top level: unexpected key {k!r}"))
    st_fails = check_stubs(home["obj"]["stubs.json"])
    fails += st_fails
    stubs = {s.get("id") for s in home["obj"]["stubs.json"].get("stubs", [])
             if isinstance(s, dict)} if not st_fails else set()
    pr_fails, register = check_principles(home["obj"]["principles.json"])
    fails += pr_fails
    rulings = home["rulings"]
    nodes = pol["polarities"]
    pol_ids = [n.get("id") for n in nodes if isinstance(n, dict)]
    pol_id_set = set(pol_ids)
    seen = set()
    resolved = {}
    for i, node in enumerate(nodes):
        where = f"polarities[{i}]"
        if not isinstance(node, dict):
            fails.append(("S-SHAPE", f"{where} is not an object"))
            continue
        nid = node.get("id") if isinstance(node.get("id"), str) else f"<{where}>"
        if nid in seen:
            fails.append(("S-DUP-ID", f"{where}: duplicate polarity id {nid!r}"))
        seen.add(nid)
        # R5 / R3 BEFORE the schema walk, so the refusal is named precisely, not "extra key"
        for k in node:
            if k not in schema.get("properties", {}):
                if "status" in k.lower():
                    fails.append(("R5-TYPED-STATUS", f"{nid}: key {k!r} — status is DERIVED with a "
                                                     f"clock (s238-D3), never typed on a node"))
                else:
                    fails.append(("R3-JUDGEMENT-FIELD", f"{nid}: key {k!r} — a node carries no "
                                                        f"free-text judgement of any name; its only "
                                                        f"judgement is a typed link (s238-D7)"))
        viol = []
        schema_validate(node, schema, nid, viol)
        for kw, path, detail in viol:
            if kw == "additionalProperties" and path.count(".") == 1:
                continue    # already named above at node level
            fails.append((name_violation(kw, path, detail), f"{path}: {detail}"))
        # R1 — every ref resolves against the LIVE registers
        parties = node.get("parties") if isinstance(node.get("parties"), list) else []
        roles = {p.get("role") for p in parties if isinstance(p, dict)}
        if len(parties) >= 2 and len(roles) < 2:
            fails.append(("S-ONE-SIDED", f"{nid}: every party stands on {sorted(roles)} — a polarity is "
                                         f"a pull between two true things (s238-D4); parties must span "
                                         f"at least two sides"))
        seen_refs = set()
        kinds = []
        for j, p in enumerate(parties):
            if not isinstance(p, dict) or not isinstance(p.get("ref"), str):
                continue
            ref = p["ref"]
            pw = f"{nid}.parties[{j}]"
            if ref in seen_refs:
                fails.append(("S-DUP-PARTY", f"{pw}: {ref!r} appears twice on one node"))
            seen_refs.add(ref)
            if not ASCII_ID.match(ref):
                kinds.append(None)
                continue          # named by the schema pattern walk (S-ID)
            if ref == nid:
                fails.append(("R1-SELF-PARTY", f"{pw}: a polarity may not be its own party"))
                kinds.append(None)
            elif ref in pol_id_set or POLARITY_ID.match(ref):
                fails.append(("R1-CIRCULAR", f"{pw}: {ref!r} is a polarity — a polarity as a party "
                                             f"of a polarity is not ruled (s238-D1 parties are "
                                             f"principle / obligation / ruling / stub)"))
                kinds.append(None)
            elif ref in register:
                g = register[ref].get("grade")
                kinds.append({"ref": ref, "role": p.get("role"),
                              "kind": "obligation" if g == OBLIGATION_GRADE else "principle",
                              "grade": g, "grade_name": GRADE_NAMES.get(g)})
            elif ref in stubs:
                kinds.append({"ref": ref, "role": p.get("role"), "kind": "stub", "grade": None,
                              "grade_name": None})
            elif ref.startswith("st-"):
                fails.append(("R1-UNDECLARED-STUB", f"{pw}: {ref!r} is spelled like a stub but is "
                                                    f"not declared in stubs.json"))
                kinds.append(None)
            elif ref in rulings:
                if rulings[ref].get("superseded_by"):
                    fails.append(("R1-SUPERSEDED", f"{pw}: ruling {ref!r} is superseded by "
                                                   f"{rulings[ref]['superseded_by']!r} — not live; "
                                                   f"point at the successor"))
                    kinds.append(None)
                else:
                    kinds.append({"ref": ref, "role": p.get("role"), "kind": "ruling", "grade": None,
                                  "grade_name": None})
            else:
                fails.append(("R1-DANGLING", f"{pw}: {ref!r} resolves to nothing — not a "
                                             f"principles.json row, not a stubs.json stub, not a "
                                             f"knowledge/_rulings.json id"))
                kinds.append(None)
        links = node.get("links") if isinstance(node.get("links"), list) else []
        seen_links = set()
        party_refs = {p.get("ref") for p in parties if isinstance(p, dict)}
        for j, l in enumerate(links):
            if not isinstance(l, dict) or not isinstance(l.get("ref"), str):
                continue
            ref = l["ref"]
            lw = f"{nid}.links[{j}]"
            key = (l.get("type"), ref)
            if key in seen_links:
                fails.append(("S-DUP-PARTY", f"{lw}: duplicate link {key!r}"))
            seen_links.add(key)
            if not ASCII_ID.match(ref):
                continue
            if ref == nid or ref in pol_id_set or POLARITY_ID.match(ref):
                fails.append(("R1-CIRCULAR", f"{lw}: {ref!r} is a polarity — a polarity→polarity "
                                             f"link is not ruled; pairwise edges are DERIVED, "
                                             f"never authored (s238-D1)"))
            elif ref in register or ref in stubs or ref.startswith("st-") or ref.startswith("pr-"):
                fails.append(("R1-WRONG-REGISTER", f"{lw}: {ref!r} is a principle/stub id — links "
                                                   f"are RULING links (s238-D6); principles are "
                                                   f"parties, not link targets"))
            elif ref in rulings:
                if rulings[ref].get("superseded_by"):
                    fails.append(("R1-SUPERSEDED", f"{lw}: ruling {ref!r} is superseded by "
                                                   f"{rulings[ref]['superseded_by']!r} — not live; "
                                                   f"point at the successor"))
            else:
                fails.append(("R1-DANGLING", f"{lw}: {ref!r} is not a knowledge/_rulings.json id"))
            if ref in party_refs:
                # ADVISORY, not a refusal: R1's own rows (pl-15, pl-16) put a ruling on one side AND
                # cite it as the route. Whether that is one fact or two is Dave's (report Q).
                pass
        # R3 — a quote must be VERBATIM from the node's own source row: a paraphrase is a judgement
        # wearing quote marks. Verified where the source is reachable; declared UNVERIFIED where not.
        fails += check_quotes_verbatim(nid, node)
        resolved[nid] = kinds
    return fails, resolved


_SOURCE_CACHE = {}
QUOTE_NOTES = []


def _source_row_text(path_rel, row_id):
    """All string values of the dict whose `id` == row_id inside the JSON at path_rel, joined;
    None when the file is unreachable / not JSON / the id is absent."""
    key = (path_rel, row_id)
    if key in _SOURCE_CACHE:
        return _SOURCE_CACHE[key]
    text = None
    path = os.path.join(REPO, path_rel)
    if os.path.isfile(path):
        try:
            obj = json.loads(read_text(path))
        except Exception:
            obj = None
        stack = [obj]
        while stack and text is None:
            cur = stack.pop()
            if isinstance(cur, dict):
                if cur.get("id") == row_id:
                    text = " ".join(str(v) for v in cur.values() if isinstance(v, str))
                    break
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
    _SOURCE_CACHE[key] = text
    return text


def check_quotes_verbatim(nid, node):
    fails = []
    links = node.get("links") if isinstance(node.get("links"), list) else []
    sources = node.get("sources") if isinstance(node.get("sources"), list) else []
    quoted = [(j, l) for j, l in enumerate(links) if isinstance(l, dict) and isinstance(l.get("quote"), str)]
    if not quoted:
        return fails
    hays = [t for t in (_source_row_text(s.get("path"), s.get("id")) for s in sources
                        if isinstance(s, dict)) if t is not None]
    if not hays:
        QUOTE_NOTES.append((len(quoted), f"{nid}: {len(quoted)} quote(s) UNVERIFIED — no source row "
                                         f"reachable at {[s.get('path') for s in sources if isinstance(s, dict)]}"))
        return fails
    for j, l in quoted:
        q = l["quote"]
        if not any(q in h for h in hays):
            fails.append(("R3-QUOTE-NOT-VERBATIM",
                          f"{nid}.links[{j}].quote: {q[:60]!r}… is not a verbatim substring of the "
                          f"node's source row — a paraphrase is a judgement wearing quote marks"))
    return fails


# ============================================================================================
# THE DERIVATION — status (with a clock), edges (pairwise view), the defaults declaration
# ============================================================================================
STATUS_RULES = {
    "R-OBLIGATION": ">=1 party resolves to a principles.json row whose grade is L (= OBLIGATION, "
                    "s237-D1; a node type no principle can outrank, s237-D2) -> settled-by-obligation. "
                    "Applied FIRST.",
    "R-RESOLVED": ">=1 link typed resolvedBy whose ref is a live ruling in knowledge/_rulings.json "
                  "-> resolved. (237-T's R-RESOLVED read how_it_resolves prose for an id; the typed "
                  "link IS that citation, migrated.)",
    "R-OPEN": "the complement.",
    "RULE-K/RULE-D": "knowable_how / disposition / ask_when / factory_default are COPIED per open row "
                     "from 237-T's open-tensions.json, FLOATED — the four ask-whens are Dave's "
                     "(s238-D3); this file rules nothing. `factory_default` is the GRILL's sense of "
                     "default (value used because nothing was asked), not s219-D3's shipped option.",
}
EDGE_RULE = ("for each polarity, for each unordered pair of parties on DIFFERENT sides whose refs both "
             "resolve to principles.json rows (principle or obligation) -> one edge carrying the "
             "polarity id and its mediating variable. Same-side pairs produce NO edge (237-T finding 4: "
             "tn-19's three persuasion principles are one side). Stubs and rulings produce NO edge "
             "(237-T finding 3: an edge needs a register node at both ends). This is a VIEW: the node "
             "is the home (s238-D1).")
DECLARE_RULE = ("D-DECLARE (s238-D5): a polarity's factory default is DECLARED iff it BENT AWAY FROM THE "
                "CONSERVATIVE SIDE — not all of them, not on demand.")


def open_defaults_rows():
    """The 237-T proposals, keyed by tn-id. Raises FileNotFoundError when the asset is unreachable."""
    with open(OPEN_DEFAULTS, "rb") as f:
        raw = f.read()
    obj = json.loads(raw.decode("utf-8"))
    return {r["id"]: r for r in obj.get("rows", [])}, sha256_bytes(raw)


def canonical(body):
    return json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def render_json(body, generated_at):
    doc = {"$header": GEN_HEADER, "generated_at": generated_at,
           "content_sha256": sha256_text(canonical(body))}
    doc.update(body)
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def render_txt(body_lines, generated_at):
    body = "\n".join(body_lines) + "\n"
    return (f"{GEN_HEADER}\ngenerated_at: {generated_at}\ncontent_sha256: {sha256_text(body)}\n"
            f"---\n{body}")


def derive(home, resolved, defaults, defaults_sha, generated_at):
    """Return {filename: text} for the three generated files, at the given clock."""
    nodes = home["obj"]["polarities.json"]["polarities"]
    rows, edges = [], []
    counts = {"settled-by-obligation": 0, "resolved": 0, "open": 0}
    kind_counts = {"principle": 0, "obligation": 0, "ruling": 0, "stub": 0}
    n_with_edges = 0
    for node in nodes:
        nid = node["id"]
        kinds = [k for k in resolved.get(nid, []) if k]
        for k in kinds:
            kind_counts[k["kind"]] += 1
        obl = [k["ref"] for k in kinds if k["kind"] == "obligation"]
        resolving = [l["ref"] for l in node.get("links", []) if l.get("type") == "resolvedBy"]
        if obl:
            status = "settled-by-obligation"
        elif resolving:
            status = "resolved"
        else:
            status = "open"
        counts[status] += 1
        r1_id = node["sources"][0]["id"] if node.get("sources") else None
        row = {"id": nid, "r1_id": r1_id, "status_derived": status,
               "obligation_parties": obl, "resolving_links": resolving,
               "parties": kinds, "links": node.get("links", []),
               "mediating_variable": node.get("mediating_variable")}
        if status == "open":
            d = defaults.get(r1_id)
            if d is None:
                row["proposal"] = "ABSENT — no row in open-tensions.json for this polarity"
                row["factory_default"] = None
            else:
                row["factory_default"] = d.get("factory_default_proposed")
                row["disposition"] = d.get("disposition")
                row["ask_when"] = d.get("ask_when")
                row["knowable_by_factory"] = d.get("knowable_by_factory")
                row["knowable_how"] = d.get("knowable_how")
                row["question_proposed"] = d.get("question_proposed")
                row["register"] = d.get("register", "FLOATED — proposed, never ruled")
        rows.append(row)
        reg_parties = [k for k in kinds if k["kind"] in ("principle", "obligation")]
        made = 0
        for a in range(len(reg_parties)):
            for b in range(a + 1, len(reg_parties)):
                pa, pb = reg_parties[a], reg_parties[b]
                if pa["role"] == pb["role"]:
                    continue
                edges.append({"polarity": nid, "from": pa["ref"], "to": pb["ref"],
                              "from_kind": pa["kind"], "to_kind": pb["kind"],
                              "mediating_variable": node.get("mediating_variable")})
                made += 1
        if made:
            n_with_edges += 1
    edges.sort(key=lambda e: (e["polarity"], e["from"], e["to"]))
    status_body = {
        "rules": STATUS_RULES,
        "counts": counts,
        "party_kinds": kind_counts,
        "delta_vs_237T": {
            "237-T_sort": T_SORT_FIGURE[0], "237-T_source": T_SORT_FIGURE[1],
            "this_derivation": f"{counts['settled-by-obligation']} · {counts['resolved']} · {counts['open']}",
            "cause": ("pl-22 (tn-22) carries resolvedBy s217-D8, whose id sat in apollo_touch (237-T "
                      "finding 2: a genuine resolution whose id sits in the wrong field). pl-02's "
                      "s217-D5 is typed `touches` (UNPROVEN — see the migration receipt), so the "
                      "6 · 9 · 15 figure quoted in s238-D6 — the naive variant that would have closed "
                      "four rows wrongly — is not reproduced, by design."),
        },
        "inputs": {"open_defaults": {"path": OPEN_DEFAULTS_REL, "sha256": defaults_sha}},
        "rows": rows,
    }
    edges_body = {
        "rule": EDGE_RULE,
        "counts": {"edges": len(edges), "polarities_with_edges": n_with_edges,
                   "polarities_without_edges": len(nodes) - n_with_edges,
                   "parties_not_edgeable": kind_counts["stub"] + kind_counts["ruling"]},
        "edges": edges,
    }
    open_rows = [r for r in rows if r["status_derived"] == "open"]
    absent = [r for r in open_rows if r.get("factory_default") is None]
    lines = [
        "DEFAULTS DECLARATION (s238-D5) — the `Defaults used:` lines the grill would carry.",
        "RULE " + DECLARE_RULE,
        "SENSE: `factory_default` is the GRILL's default (the value used because nothing was asked),",
        "       not s219-D3's shipped-option default — two senses already exist, so the field is named.",
        f"SOURCE OF \"WHICH SIDE IS CONSERVATIVE\": {OPEN_DEFAULTS_REL} (sha256 {defaults_sha[:16]}…)",
        "       carries NO per-row field for it. Its generator's docstring (_derive_open_table.py)",
        "       asserts every factory_default_proposed \"takes the conservative side\" — prose, not a",
        "       per-row datum. RULE APPLIED: bent = UNKNOWN for every row => nothing can be declared",
        "       as bent => 0 declared; every open row is UNPROVEN until the conservative side is",
        "       carried as data (Dave's).",
        f"open polarities: {len(open_rows)} · declared: 0 · UNPROVEN: {len(open_rows) - len(absent)} · "
        f"no proposal in the source: {len(absent)}",
        "Defaults used:",
        f"  (none — 0 of {len(open_rows)} bent from the conservative side; see UNPROVEN)",
        "UNPROVEN (conservative side not carried as data; the default text stays FLOATED in the source",
        "          and in polarity-status.json, it is NOT declared here):",
    ]
    for r in open_rows:
        if r.get("factory_default") is None:
            lines.append(f"  {r['id']} ({r['r1_id']}) NO PROPOSAL — {r.get('proposal')}")
        else:
            lines.append(f"  {r['id']} ({r['r1_id']}) {r.get('disposition')} — ask when: {r.get('ask_when')}")
    return {
        "polarity-status.json": render_json(status_body, generated_at),
        "polarity-edges.json": render_json(edges_body, generated_at),
        "defaults-declaration.txt": render_txt(lines, generated_at),
    }, counts, kind_counts, len(edges), len(open_rows)


# ============================================================================================
# FRESHNESS — content, never mtime; hand-written is a different verdict from stale
# ============================================================================================
def read_generated(brain, name):
    """(generated_at, self_ok, text) or raises Refused MISSING / R4-AUTHORED-GENERATED."""
    path = os.path.join(brain, GEN_DIR, name)
    if not os.path.exists(path):
        raise Refused("MISSING-GENERATED", f"{GEN_DIR}/{name} is absent — run: python3 "
                                           f"knowledge/_validate_polarities.py --write")
    text = read_text(path)
    if name.endswith(".json"):
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as e:
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name} does not parse ({e}) — a "
                                                   f"generated file that does not parse was hand-"
                                                   f"written; delete it and run --write")
        if not isinstance(obj, dict) or obj.get("$header") != GEN_HEADER:
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name} lacks the header "
                                                   f"{GEN_HEADER!r} — an AUTHORED file at a generated "
                                                   f"path (s238-D7 refusal 4); delete it and run --write")
        gen_at = obj.get("generated_at")
        body = {k: v for k, v in obj.items() if k not in ("$header", "generated_at", "content_sha256")}
        if obj.get("content_sha256") != sha256_text(canonical(body)):
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: content_sha256 does not match "
                                                   f"its own body — the file was HAND-EDITED after "
                                                   f"generation (s238-D7 refusal 4); delete it and run "
                                                   f"--write")
        return gen_at, text
    lines = text.split("\n")
    if len(lines) < 4 or lines[0] != GEN_HEADER or not lines[1].startswith("generated_at: ") \
            or not lines[2].startswith("content_sha256: ") or lines[3] != "---":
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name} lacks the generated header block — "
                                               f"an AUTHORED file at a generated path (s238-D7 "
                                               f"refusal 4); delete it and run --write")
    body = "\n".join(lines[4:])
    if lines[2][len("content_sha256: "):] != sha256_text(body):
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: content_sha256 does not match its "
                                               f"own body — HAND-EDITED after generation (s238-D7 "
                                               f"refusal 4); delete it and run --write")
    return lines[1][len("generated_at: "):], text


def freshness(brain, home, resolved, defaults, defaults_sha):
    fails, notes = [], []
    for name in GEN_FILES:
        try:
            gen_at, on_disk = read_generated(brain, name)
        except Refused as r:
            fails.append((r.name, r.detail))
            continue
        fresh, *_ = derive(home, resolved, defaults, defaults_sha, gen_at)
        if fresh[name] != on_disk:
            fails.append(("STALE-GENERATED", f"{GEN_DIR}/{name} does not match a fresh derivation "
                                             f"(content compared at its own clock {gen_at}) — run: "
                                             f"python3 knowledge/_validate_polarities.py --write"))
        else:
            notes.append(f"{GEN_DIR}/{name} fresh (generated_at {gen_at}, content byte-identical)")
    return fails, notes


# ============================================================================================
# THE GATE — one entry point for the build, the seam, the writer and every selftest arm
# ============================================================================================
def print_refusals(fails, brain):
    print(f"⛔ POLARITY GATE REFUSED — {len(fails)} refusal(s) over {brain} (nothing written):")
    for name, detail in fails:
        print(f"   ⛔ REFUSED ({name}) — {detail}")


def gate(brain, write=False, overrides=None, quiet=False):
    """The whole contract. Returns rc. Prints. Never raises on a refusal."""
    say = (lambda *a, **k: None) if quiet else print
    fails = []
    QUOTE_NOTES.clear()
    _SOURCE_CACHE.clear()
    if not os.path.isdir(brain):
        # #173 / #193 — the honest third verdict: the INPUT is not here (a shipped pack does not
        # carry knowledge/brain/), so the question is unaskable, not failed. Spelled so the pack
        # classifier's `_unshipped_subject` reads it as REPO-BOUND (a "does not exist" + the path).
        return cna.refuse(os.path.join(os.path.relpath(brain, REPO) if brain.startswith(REPO) else brain,
                                       "polarities.json"),
                          f"the polarity home {os.path.relpath(brain, REPO) if brain.startswith(REPO) else brain}/ "
                          f"does not exist here — knowledge/brain/ is a repo resource a shipped pack does "
                          f"not carry, so the five refusals cannot be asked. Run from the source repo.")
    try:
        fails += check_home_dir(brain)
        home = load_home(brain, overrides)
        pf, resolved = check_polarities(home)
        fails += pf
    except Refused as r:
        fails.append((r.name, r.detail))
        print_refusals(fails, brain)
        return 1
    if fails:
        print_refusals(fails, brain)
        return 1
    try:
        defaults, defaults_sha = open_defaults_rows()
    except FileNotFoundError:
        return cna.refuse("knowledge/brain/_generated/polarity-status.json",
                          f"the five refusals PASSED on {brain}, but the defaults declaration derives "
                          f"from {OPEN_DEFAULTS_REL}, which does not exist here (it lives outside "
                          f"knowledge/; a shipped pack does not carry it). Freshness is UNASKED, not "
                          f"passed. Run from the source repo.")
    nodes = home["obj"]["polarities.json"]["polarities"]
    if write:
        texts, counts, kinds, n_edges, n_open = derive(home, resolved, defaults, defaults_sha, now_clock())
        gen_dir = os.path.join(brain, GEN_DIR)
        os.makedirs(gen_dir, exist_ok=True)
        # an AUTHORED file at a generated path is refused even by --write: nothing is blown away
        for name in GEN_FILES:
            if os.path.exists(os.path.join(gen_dir, name)):
                try:
                    read_generated(brain, name)
                except Refused as r:
                    if r.name == "R4-AUTHORED-GENERATED":
                        fails.append((r.name, r.detail))
        if fails:
            print_refusals(fails, brain)
            return 1
        for name in GEN_FILES:
            tmp = os.path.join(gen_dir, "." + name + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(texts[name])
            os.replace(tmp, os.path.join(gen_dir, name))
        say(f"WROTE {len(GEN_FILES)} generated file(s) under {os.path.relpath(gen_dir, REPO)}/ "
            f"(generated_at {json.loads(texts['polarity-status.json'])['generated_at']})")
    ff, notes = freshness(brain, home, resolved, defaults, defaults_sha)
    _, counts, kinds, n_edges, n_open = derive(home, resolved, defaults, defaults_sha, "clock-held")
    n_links = sum(len(n.get("links", [])) for n in nodes)
    by_type = {}
    for n in nodes:
        for l in n.get("links", []):
            by_type[l["type"]] = by_type.get(l["type"], 0) + 1
    say(f"polarity gate (s238-D7): home {os.path.relpath(brain, REPO) if brain.startswith(REPO) else brain} · "
        f"rows {len(nodes)} · parties {sum(kinds.values())} "
        f"(principle {kinds['principle']} · obligation {kinds['obligation']} · ruling {kinds['ruling']} · "
        f"stub {kinds['stub']}) · stubs declared {len(home['obj']['stubs.json']['stubs'])} · "
        f"links {n_links} by type " + " ".join(f"{k}={v}" for k, v in sorted(by_type.items()))
        + " · refusals asked: R1 R2 R3 R4 R5 — none fired")
    n_quotes = sum(1 for n in nodes for l in n.get("links", []) if isinstance(l.get("quote"), str))
    n_unverified = sum(c for c, _ in QUOTE_NOTES)
    say(f"  quotes {n_quotes}: verbatim against their source rows — {n_quotes - n_unverified} verified, "
        f"{n_unverified} UNVERIFIED (declared, not passed)")
    for _c, qn in QUOTE_NOTES:
        say(f"  ⚠ {qn}")
    for k, v in STATUS_RULES.items():
        say(f"  RULE {k}: {v}")
    say(f"  status derived: settled-by-obligation {counts['settled-by-obligation']} · resolved "
        f"{counts['resolved']} · open {counts['open']}   (237-T at its clock: {T_SORT_FIGURE[0]})")
    say(f"  RULE EDGES: {EDGE_RULE}")
    say(f"  edges derived: {n_edges}")
    say(f"  {DECLARE_RULE}  open {n_open} · declared 0 · UNPROVEN {n_open} (conservative side not "
        f"carried as data)")
    for n in notes:
        say(f"  ✓ {n}")
    if ff:
        print_refusals(ff, brain)
        return 1
    say("✓ polarity gate GREEN — five refusals asked and none fired; generated files content-fresh")
    return 0


# ============================================================================================
# THE WRITER — textual append into the home, proven by reconstruction (the _inscribe_ruling shape)
# ============================================================================================
def _array_bounds(text, key):
    """(open_index, close_index) of the `key` array, found by a string-aware depth scan."""
    start = text.index(f'"{key}"')
    i = text.index("[", start)
    depth, in_str, esc = 0, False, False
    for j in range(i, len(text)):
        c = text[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                return i, j
    raise Refused("S-SHAPE", f"could not find the close of the `{key}` array")


def compose_append(text, key, entry):
    """(new_text, at, span). Serialises ONLY the new entry; every other byte is carried through."""
    open_i, close = _array_bounds(text, key)
    inside = text[open_i + 1:close]
    body = json.dumps(entry, indent=1, ensure_ascii=False)
    body = "\n".join(" " + ln for ln in body.splitlines())
    if inside.strip() == "":
        span, at = "\n" + body + "\n", open_i + 1
    else:
        last_brace = open_i + 1 + inside.rindex("}")
        span, at = ",\n" + body, last_brace + 1
    return text[:at] + span + text[at:], at, span


def add_entry(brain, which, entry, write):
    """which ∈ {'polarity','stub'}. Returns rc; prints the proof or the refusal."""
    fname, key = ("polarities.json", "polarities") if which == "polarity" else ("stubs.json", "stubs")
    path = os.path.join(brain, fname)
    original = read_text(path)
    try:
        new_text, at, span = compose_append(original, key, entry)
    except Refused as r:
        print(f"⛔ REFUSED ({r.name}) — {r.detail}. File untouched.")
        return 1
    if new_text[:at] + new_text[at + len(span):] != original:            # the reconstruction proof
        print("⛔ REFUSED (NOT-TEXTUAL) — removing the inserted span does not give back the original "
              "bytes; something reformatted the file (the #179 defect). File untouched.")
        return 1
    try:
        after = json.loads(new_text)
    except json.JSONDecodeError as e:
        print(f"⛔ REFUSED (S-PARSE) — the composed text does not parse: {e}. File untouched.")
        return 1
    before_n = len(json.loads(original)[key])
    if len(after[key]) != before_n + 1 or after[key][-1] != entry:
        print("⛔ REFUSED (ROUND-TRIP) — the result does not carry exactly one more entry equal to the "
              "one submitted. File untouched.")
        return 1
    # THE WHOLE GATE, on the resulting text, BEFORE a byte is written. The derived files are
    # EXPECTED to read stale against the appended home (nothing has re-derived them yet), so that
    # one verdict is folded into the write step; every other refusal stands and stops the append.
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = gate(brain, write=False, overrides={fname: new_text}, quiet=True)
    finally:
        sys.stdout = old
    only_stale = rc == 1 and _only_stale(brain, {fname: new_text})
    if rc != 0 and not only_stale:
        print(buf.getvalue(), end="")
        print(f"⛔ the gate REFUSED the home as it would stand after this append (rc {rc}) — see "
              f"the refusals above. File untouched.")
        return 1
    print(f"✓ append proven textual: {fname} +{len(span)} bytes at byte {at}; reconstruction == "
          f"original; parses to {before_n + 1} entries; the five refusals pass on the result"
          + ("; the derived files will re-derive on --write" if only_stale else ""))
    if not write:
        print("  (dry run — nothing written; pass --write to write and regenerate)")
        return 0
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new_text)
    os.replace(tmp, path)
    print(f"WROTE {os.path.relpath(path, REPO)}; regenerating the derived files:")
    return gate(brain, write=True)


def _only_stale(brain, overrides):
    """True when the ONLY refusals over the overridden home are STALE-GENERATED (expected: the
    append has not been derived yet)."""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        home = load_home(brain, overrides)
        pf, resolved = check_polarities(home)
        if pf or check_home_dir(brain):
            return False
        defaults, sha = open_defaults_rows()
        ff, _ = freshness(brain, home, resolved, defaults, sha)
        return all(n == "STALE-GENERATED" for n, _ in ff)
    except Exception:
        return False
    finally:
        sys.stdout = old


# ============================================================================================
# SELFTEST — control + one arm per refusal + extras, ALL driven through gate() (the same entry
# point the build and the commit seam call) on a COPY of the REAL rows. Every arm must go RED
# by its NAME; a crash is not a fail.
# ============================================================================================
def _copy_brain(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".*.tmp"))


def _mutate_json(path, fn):
    obj = json.loads(read_text(path))
    fn(obj)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def _run_gate_captured(brain, write=False, overrides=None):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        try:
            rc = gate(brain, write=write, overrides=overrides)
        except Exception:               # a crash is not a fail — surface it as one, named
            rc = -1
            buf.write("TRACEBACK\n" + traceback.format_exc())
    finally:
        sys.stdout = old
    return rc, buf.getvalue()


def _tree_hashes(root):
    out = {}
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            with open(p, "rb") as f:
                out[os.path.relpath(p, root)] = sha256_bytes(f.read())
    return out


def selftest(real_brain):
    results = []          # (n, arm, expected, rc, named?, ok, note)
    tmp_root = tempfile.mkdtemp(prefix="polarity-selftest-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)

    def arm(name, expect, mutate, must_name=None, write=False):
        """Copy the REAL brain, apply `mutate(copy_dir)`, drive gate(--check) on it."""
        n = len(results) + 1
        d = os.path.join(tmp_root, f"arm{n:02d}")
        _copy_brain(real_brain, d)
        before = _tree_hashes(d)
        try:
            mutate(d)
        except Exception as e:
            results.append((n, name, expect, None, False, False, f"mutation setup crashed: {e}"))
            return
        after_mut = _tree_hashes(d)
        rc, out = _run_gate_captured(d, write=write)
        after = _tree_hashes(d)
        crashed = "TRACEBACK" in out
        named = bool(must_name) and (f"REFUSED ({must_name})" in out or must_name in out)
        if expect == "green":
            ok = rc == 0 and not crashed
            note = "" if ok else out[-600:]
        else:
            untouched = (after == after_mut)
            ok = (rc == 1) and named and not crashed and untouched
            note = ("" if ok else f"rc={rc} named={named} crashed={crashed} untouched={untouched} :: "
                                  + out[-500:])
        results.append((n, name, expect, rc, named, ok, note))
        return d

    def pol(fn):
        return lambda d: _mutate_json(os.path.join(d, "polarities.json"), fn)

    def stubs(fn):
        return lambda d: _mutate_json(os.path.join(d, "stubs.json"), fn)

    # ---- CONTROL ------------------------------------------------------------------------------
    arm("CONTROL: the real 30 rows, untouched", "green", lambda d: None)

    # ---- R1 -----------------------------------------------------------------------------------
    arm("R1 dangling PARTY ref (pr-does-not-exist)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pr-does-not-exist", "role": "side_b"})),
        "R1-DANGLING")
    arm("R1 dangling LINK ref (s999-D9)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "s999-D9"})),
        "R1-DANGLING")
    rulings_now = json.loads(read_text(RULINGS))["rulings"]
    superseded = [r["id"] for r in rulings_now if isinstance(r, dict) and r.get("superseded_by")]
    if superseded:
        arm(f"R1 link to a SUPERSEDED ruling ({superseded[0]}, real store)", "red",
            pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": superseded[0]})),
            "R1-SUPERSEDED")
        arm(f"R1 PARTY that is a superseded ruling ({superseded[0]})", "red",
            pol(lambda o: o["polarities"][0]["parties"].append({"ref": superseded[0], "role": "side_b"})),
            "R1-SUPERSEDED")
    else:
        results.append((len(results) + 1, "R1 superseded ruling arm", "red", None, False, False,
                        "no ruling in knowledge/_rulings.json carries `superseded_by` — the arm cannot "
                        "be driven on real data; UNPROVEN, not passed"))
    arm("R1 SELF-PARTY (pl-01 lists itself)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pl-01", "role": "side_b"})),
        "R1-SELF-PARTY")
    arm("R1 CIRCULAR polarity→polarity LINK (pl-01 → pl-02)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "pl-02"})),
        "R1-CIRCULAR")
    arm("R1 CIRCULAR polarity as a PARTY of another (pl-02 on pl-01)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pl-02", "role": "side_b"})),
        "R1-CIRCULAR")
    arm("R1 link to a PRINCIPLE id (wrong register)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "pr-fitts"})),
        "R1-WRONG-REGISTER")
    arm("R1 undeclared STUB (st-not-declared)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "st-not-declared", "role": "side_b"})),
        "R1-UNDECLARED-STUB")
    arm("R1 a declared stub REMOVED from stubs.json (pl-05's party dangles)", "red",
        stubs(lambda o: o["stubs"].__delitem__(next(i for i, s in enumerate(o["stubs"])
                                                    if s["id"] == "st-input-validation-and-security"))),
        "R1-UNDECLARED-STUB")
    homoglyph = "pr-jakobs-law".replace("a", "а")     # Cyrillic а — looks identical, is not ASCII
    assert homoglyph != "pr-jakobs-law", "selftest setup: the homoglyph mutation produced no change"
    arm("R1 homoglyph ref (Cyrillic а in pr-jakobs-law) — non-ASCII id", "red",
        pol(lambda o: o["polarities"][1]["parties"].append({"ref": homoglyph, "role": "side_b"})),
        "S-ID")

    # ---- R2 -----------------------------------------------------------------------------------
    arm("R2 UNTYPED link (type key absent)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"ref": "s116-D1"})),
        "R2-UNTYPED")
    arm("R2 UNKNOWN (fifth) link type `relatedTo`", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "relatedTo", "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")
    arm("R2 link type wrong case `ResolvedBy`", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "ResolvedBy", "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")
    arm("R2 link type empty string", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "", "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")

    # ---- R3 -----------------------------------------------------------------------------------
    arm("R3 judgement field `how_it_resolves` on a node", "red",
        pol(lambda o: o["polarities"][0].__setitem__("how_it_resolves", "Never trade them at the same layer.")),
        "R3-JUDGEMENT-FIELD")
    arm("R3 judgement field of ANOTHER name (`verdict`)", "red",
        pol(lambda o: o["polarities"][3].__setitem__("verdict", "aesthetics wins")),
        "R3-JUDGEMENT-FIELD")
    arm("R3 judgement smuggled into a link `quote` (16 words)", "red",
        pol(lambda o: o["polarities"][0]["links"].append(
            {"type": "touches", "ref": "s116-D1", "quote": " ".join(["word"] * 16)})),
        "R3-QUOTE-TOO-LONG")
    arm("R3 judgement smuggled into a party `note` (16 words)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", " ".join(["word"] * 16))),
        "R3-NOTE-TOO-LONG")
    arm("R3 judgement field inside a PARTY object (`why`)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("why", "because")),
        "R3-JUDGEMENT-FIELD")
    arm("R3 stub with a third key (`rationale`)", "red",
        stubs(lambda o: o["stubs"][0].__setitem__("rationale", "x")),
        "S-STUB-SHAPE")
    arm("R3 link quote PARAPHRASED (not verbatim in the source row)", "red",
        pol(lambda o: o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget")),
        "R3-QUOTE-NOT-VERBATIM")

    # ---- R4 -----------------------------------------------------------------------------------
    def authored_edges_at_generated_path(d):
        with open(os.path.join(d, GEN_DIR, "polarity-edges.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps({"edges": [{"from": "pr-fitts", "to": "pr-hick"}]}, indent=1) + "\n")
    arm("R4 AUTHORED file at the generated path (no header)", "red",
        authored_edges_at_generated_path, "R4-AUTHORED-GENERATED")

    def hand_edited_generated(d):
        p = os.path.join(d, GEN_DIR, "polarity-status.json")
        obj = json.loads(read_text(p))
        obj["rows"][0]["status_derived"] = "resolved"        # header kept, body changed by hand
        with open(p, "w", encoding="utf-8") as f:
            f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    arm("R4 generated file HAND-EDITED under its header (self-sha breaks)", "red",
        hand_edited_generated, "R4-AUTHORED-GENERATED")

    def authored_edges_beside_homes(d):
        with open(os.path.join(d, "edges.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps({"edges": []}) + "\n")
    arm("R4 AUTHORED edge file beside the homes (knowledge/brain/edges.json)", "red",
        authored_edges_beside_homes, "R4-AUTHORED-EDGES")

    def stray_file(d):
        with open(os.path.join(d, "polarities-v2.json"), "w", encoding="utf-8") as f:
            f.write("{}\n")
    arm("R4 STRAY second shape beside the homes (polarities-v2.json)", "red", stray_file, "R4-STRAY-FILE")

    def stray_inside_generated(d):
        with open(os.path.join(d, GEN_DIR, "polarity-edges-extra.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps({"edges": []}) + "\n")
    arm("R4 AUTHORED file INSIDE _generated/ beside the derived three", "red",
        stray_inside_generated, "R4-STRAY-FILE")

    def txt_hand_edited(d):
        p = os.path.join(d, GEN_DIR, "defaults-declaration.txt")
        t = read_text(p).replace("Defaults used:\n", "Defaults used:\n  pl-01 — converge on mechanism\n")
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
    arm("R4 defaults-declaration.txt HAND-EDITED (a default declared by hand)", "red",
        txt_hand_edited, "R4-AUTHORED-GENERATED")

    # ---- R5 -----------------------------------------------------------------------------------
    arm("R5 typed `status` on a node", "red",
        pol(lambda o: o["polarities"][0].__setitem__("status", "open")), "R5-TYPED-STATUS")
    arm("R5 typed status under another spelling (`derivedStatus`)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("derivedStatus", "resolved")), "R5-TYPED-STATUS")

    # ---- SCHEMA EXTRAS -------------------------------------------------------------------------
    arm("S 1 party (minItems 2)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("parties", o["polarities"][0]["parties"][:1])),
        "S-MIN-PARTIES")
    arm("S DUPLICATE party (same ref twice on pl-01)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append(dict(o["polarities"][0]["parties"][0]))),
        "S-DUP-PARTY")
    arm("S DUPLICATE polarity id", "red",
        pol(lambda o: o["polarities"].append(dict(o["polarities"][0]))), "S-DUP-ID")
    arm("S unicode polarity id (fullwidth digit)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("id", "pl-0１")), "S-ID")
    arm("S party role outside the enum (`side_d`)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", "side_d")), "S-ROLE")
    arm("S ONE-SIDED: every party on side_a (no pull)", "red",
        pol(lambda o: [p.__setitem__("role", "side_a") for p in o["polarities"][0]["parties"]]),
        "S-ONE-SIDED")
    arm("S mediating_variable empty", "red",
        pol(lambda o: o["polarities"][0].__setitem__("mediating_variable", "")), "S-SCHEMA")
    arm("S sources missing", "red",
        pol(lambda o: o["polarities"][0].__delitem__("sources")), "S-SCHEMA")
    arm("S polarities.json does not parse", "red",
        lambda d: open(os.path.join(d, "polarities.json"), "a").write("{"), "S-PARSE")

    # ---- FRESHNESS -----------------------------------------------------------------------------
    def stale(d):
        # a REAL edit to the home (a new touches link) with no --write: the derived files go stale
        _mutate_json(os.path.join(d, "polarities.json"),
                     lambda o: o["polarities"][5]["links"].append({"type": "touches", "ref": "s116-D1"}))
    arm("FRESHNESS: home edited, generated files not re-derived → STALE", "red", stale, "STALE-GENERATED")
    arm("FRESHNESS: a generated file deleted → MISSING", "red",
        lambda d: os.remove(os.path.join(d, GEN_DIR, "polarity-edges.json")), "MISSING-GENERATED")

    # ---- WRITE PATH ----------------------------------------------------------------------------
    d_w = os.path.join(tmp_root, "write-refused")
    _copy_brain(real_brain, d_w)
    _mutate_json(os.path.join(d_w, "polarities.json"),
                 lambda o: o["polarities"][0].__setitem__("status", "open"))
    gen_before = _tree_hashes(os.path.join(d_w, GEN_DIR))
    rc, out = _run_gate_captured(d_w, write=True)
    gen_after = _tree_hashes(os.path.join(d_w, GEN_DIR))
    ok = rc == 1 and "R5-TYPED-STATUS" in out and gen_before == gen_after
    results.append((len(results) + 1, "WRITE: --write on a refused home writes NOTHING (hashes equal)",
                    "red", rc, "R5-TYPED-STATUS" in out, ok, "" if ok else out[-400:]))

    d_s = os.path.join(tmp_root, "write-stale-then-fresh")
    _copy_brain(real_brain, d_s)
    stale(d_s)
    rc1, _ = _run_gate_captured(d_s)                       # stale → red
    rc2, out2 = _run_gate_captured(d_s, write=True)        # write → green
    rc3, _ = _run_gate_captured(d_s)                       # check → green, idempotent
    ok = rc1 == 1 and rc2 == 0 and rc3 == 0
    results.append((len(results) + 1, "WRITE: stale → --write → fresh (rc 1 → 0 → 0)", "green",
                    rc3, True, ok, "" if ok else f"rc {rc1},{rc2},{rc3} :: {out2[-300:]}"))
    # the clock is HELD by --check: two writes differ only in generated_at
    t1 = read_text(os.path.join(d_s, GEN_DIR, "polarity-status.json"))
    rc4, _ = _run_gate_captured(d_s, write=True)
    t2 = read_text(os.path.join(d_s, GEN_DIR, "polarity-status.json"))
    strip = lambda t: re.sub(r'"generated_at": "[^"]*"', '"generated_at": "X"', t)
    ok = rc4 == 0 and strip(t1) == strip(t2)
    results.append((len(results) + 1, "WRITE: determinism — two writes differ only in generated_at",
                    "green", rc4, True, ok, "" if ok else "bodies differ"))

    # ---- THE TEXTUAL WRITER (--add-*) ------------------------------------------------------------
    d_a = os.path.join(tmp_root, "add-polarity")
    _copy_brain(real_brain, d_a)
    good = {"id": "pl-99", "parties": [{"ref": "pr-fitts", "role": "side_a"},
                                       {"ref": "pr-hick", "role": "side_b"}],
            "mediating_variable": "selftest only", "links": [], "sources": [{"path": "selftest", "id": "x"}]}
    orig = read_text(os.path.join(d_a, "polarities.json"))
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_dry = add_entry(d_a, "polarity", good, write=False)
        untouched = read_text(os.path.join(d_a, "polarities.json")) == orig
        rc_wr = add_entry(d_a, "polarity", good, write=True)
    finally:
        sys.stdout = old
    new = read_text(os.path.join(d_a, "polarities.json"))
    # reconstruction on the REAL written file, computed INDEPENDENTLY of the writer: the new text
    # must be <common prefix> + <one span> + <common suffix> with prefix + suffix == the original
    p = 0
    while p < len(orig) and p < len(new) and orig[p] == new[p]:
        p += 1
    s = len(orig) - p
    recon_ok = (len(new) > len(orig) and new[:p] + new[len(new) - s:] == orig
                and len(json.loads(new)["polarities"]) == 31 and json.loads(new)["polarities"][-1] == good)
    rc_chk, _ = _run_gate_captured(d_a)
    ok = rc_dry == 0 and untouched and rc_wr == 0 and recon_ok and rc_chk == 0
    results.append((len(results) + 1, "ADD-POLARITY: dry-run leaves bytes; --write = original + one span; "
                                      "31 rows; gate green after", "green", rc_chk, True, ok,
                    "" if ok else f"dry={rc_dry} untouched={untouched} wr={rc_wr} recon={recon_ok} chk={rc_chk} :: {buf.getvalue()[-400:]}"))

    d_b = os.path.join(tmp_root, "add-polarity-refused")
    _copy_brain(real_brain, d_b)
    bad = dict(good, id="pl-98", status="open")
    orig_b = _tree_hashes(d_b)
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_bad = add_entry(d_b, "polarity", bad, write=True)
    finally:
        sys.stdout = old
    ok = rc_bad == 1 and "R5-TYPED-STATUS" in buf.getvalue() and _tree_hashes(d_b) == orig_b
    results.append((len(results) + 1, "ADD-POLARITY: an entry with a typed status is REFUSED by name, "
                                      "nothing written", "red", rc_bad, "R5-TYPED-STATUS" in buf.getvalue(), ok,
                    "" if ok else buf.getvalue()[-400:]))

    d_c = os.path.join(tmp_root, "add-stub")
    _copy_brain(real_brain, d_c)
    orig_c = read_text(os.path.join(d_c, "stubs.json"))
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_st = add_entry(d_c, "stub", {"id": "st-selftest-phrase", "phrase": "a selftest phrase"}, write=True)
        rc_st_bad = add_entry(d_c, "stub", {"id": "st-bad", "phrase": "x", "why": "y"}, write=True)
    finally:
        sys.stdout = old
    new_c = read_text(os.path.join(d_c, "stubs.json"))
    ok = (rc_st == 0 and len(json.loads(new_c)["stubs"]) == len(json.loads(orig_c)["stubs"]) + 1
          and rc_st_bad == 1 and "S-STUB-SHAPE" in buf.getvalue())
    results.append((len(results) + 1, "ADD-STUB: good stub appended textually; 3-key stub REFUSED (S-STUB-SHAPE)",
                    "green", rc_st, True, ok, "" if ok else buf.getvalue()[-400:]))

    # ---- BITE THE BITE: the SCHEMA drives the check — loosen it and the 1-party arm must stay GREEN
    d_m = os.path.join(tmp_root, "schema-mutant")
    _copy_brain(real_brain, d_m)
    _mutate_json(os.path.join(d_m, SCHEMA_REL), lambda s: s["properties"]["parties"].pop("minItems"))
    _mutate_json(os.path.join(d_m, "polarities.json"),
                 lambda o: o["polarities"][0].__setitem__("parties", o["polarities"][0]["parties"][:1]))
    rc_m, out_m = _run_gate_captured(d_m)
    # (it goes STALE, because the edges/status change with one party gone — but NOT S-MIN-PARTIES)
    ok = "S-MIN-PARTIES" not in out_m and "TRACEBACK" not in out_m
    results.append((len(results) + 1, "BITE-THE-BITE: with minItems removed from the SCHEMA the 1-party "
                                      "refusal does NOT fire — the schema file drives the check", "nofire",
                    rc_m, False, ok, "" if ok else out_m[-300:]))
    d_k = os.path.join(tmp_root, "schema-unknown-keyword")
    _copy_brain(real_brain, d_k)
    _mutate_json(os.path.join(d_k, SCHEMA_REL), lambda s: s["properties"]["parties"].__setitem__("maxItems", 9))
    rc_k, out_k = _run_gate_captured(d_k)
    ok = rc_k == 1 and "SCHEMA-KEYWORD-UNSUPPORTED" in out_k
    results.append((len(results) + 1, "SCHEMA: a keyword this gate does not implement (maxItems) is REFUSED, "
                                      "never silently ignored", "red", rc_k, ok, ok, "" if ok else out_k[-300:]))

    # ---- CLI: the SAME entry point via subprocess, rc observed from the process --------------
    d_cli = os.path.join(tmp_root, "cli-red")
    _copy_brain(real_brain, d_cli)
    _mutate_json(os.path.join(d_cli, "polarities.json"),
                 lambda o: o["polarities"][0]["links"].append({"ref": "s116-D1"}))
    r_green = subprocess.run([sys.executable, os.path.abspath(__file__), "--check", "--brain", real_brain],
                             capture_output=True, text=True)
    r_red = subprocess.run([sys.executable, os.path.abspath(__file__), "--check", "--brain", d_cli],
                           capture_output=True, text=True)
    r_env = subprocess.run([sys.executable, os.path.abspath(__file__), "--check"],
                           capture_output=True, text=True, env=dict(os.environ, POLARITY_BRAIN_DIR=d_cli))
    ok = (r_green.returncode == 0 and r_red.returncode == 1 and "R2-UNTYPED" in r_red.stdout
          and r_env.returncode == 1 and "R2-UNTYPED" in r_env.stdout)
    results.append((len(results) + 1, "CLI: `--check` rc 0 on the real home, rc 1 + R2-UNTYPED on the mutant "
                                      "(via --brain AND via POLARITY_BRAIN_DIR)", "green", r_green.returncode,
                    True, ok, "" if ok else (r_green.stdout + r_red.stdout + r_env.stdout)[-500:]))
    r_bare = subprocess.run([sys.executable, os.path.abspath(__file__)], capture_output=True, text=True)
    r_junk = subprocess.run([sys.executable, os.path.abspath(__file__), "--wat"], capture_output=True, text=True)
    ok = r_bare.returncode == 2 and r_junk.returncode == 2 and "REFUSED" in (r_junk.stdout + r_junk.stderr)
    results.append((len(results) + 1, "CLI: bare and unknown argv refuse with rc 2 (argv contract, #208 class)",
                    "red", r_junk.returncode, ok, ok, "" if ok else (r_bare.stdout + r_junk.stdout + r_junk.stderr)[-300:]))

    # ---- THE THIRD VERDICT (#193): take the INPUT away → 77 + COULD-NOT-ASK, never 1, never 0 ----
    r77 = subprocess.run([sys.executable, os.path.abspath(__file__), "--check", "--brain",
                          os.path.join(tmp_root, "no-such-home")], capture_output=True, text=True)
    ok = r77.returncode == cna.EXIT and r77.stdout.startswith(cna.MARKER) and "does not exist" in r77.stdout
    results.append((len(results) + 1, "COULD-NOT-ASK: home directory absent → rc 77 + marker naming the path "
                                      "(pack classifier reads it as REPO-BOUND)", "77", r77.returncode, ok, ok,
                    "" if ok else r77.stdout[-300:] + r77.stderr[-300:]))
    # the declaration source (a notes/ asset) taken away: refusals still asked FIRST (a real red
    # stays red), then 77 on a clean home — proven by pointing OPEN_DEFAULTS at nothing in-process
    global OPEN_DEFAULTS
    kept = OPEN_DEFAULTS
    try:
        OPEN_DEFAULTS = os.path.join(tmp_root, "no-such-open-tensions.json")
        d77 = os.path.join(tmp_root, "src-absent-clean")
        _copy_brain(real_brain, d77)
        rc_a, out_a = _run_gate_captured(d77)
        d77b = os.path.join(tmp_root, "src-absent-red")
        _copy_brain(real_brain, d77b)
        _mutate_json(os.path.join(d77b, "polarities.json"),
                     lambda o: o["polarities"][0].__setitem__("status", "open"))
        rc_b, out_b = _run_gate_captured(d77b)
    finally:
        OPEN_DEFAULTS = kept
    ok = rc_a == cna.EXIT and cna.MARKER in out_a and rc_b == 1 and "R5-TYPED-STATUS" in out_b
    results.append((len(results) + 1, "COULD-NOT-ASK: declaration source absent → 77 on a clean home, but a "
                                      "real refusal is STILL rc 1 first (the refusal path is not swallowed)",
                    "77", rc_a, ok, ok, "" if ok else f"rc {rc_a}/{rc_b} :: {out_a[-200:]} :: {out_b[-200:]}"))

    # ---- WIRING PRESENCE (declared skip when a surface is unreachable) --------------------------
    build = os.path.join(HERE, "_build_all.py")
    seam = os.path.join(HERE, "_git_commit.sh")
    harness = os.path.join(HERE, "_test_git_commit.py")
    if os.path.exists(build) and os.path.exists(seam) and os.path.exists(harness):
        bt, st_, ht = read_text(build), read_text(seam), read_text(harness)
        ok_b = ('"_validate_polarities.py", ["--check"]' in bt and '"_validate_polarities.py", ["--selftest"]' in bt)
        seam_lines = [ln for ln in st_.splitlines() if not ln.lstrip().startswith("#")
                      and "python3 knowledge/_validate_polarities.py --check" in ln]
        ok_s = len(seam_lines) >= 1
        ok_h = 'write(os.path.join(know, "_validate_polarities.py")' in ht
        ok = ok_b and ok_s and ok_h
        results.append((len(results) + 1, "WIRING: STEPS has --check + --selftest rows; _git_commit.sh invokes "
                                          "--check on a live line; the seam harness stubs it", "green",
                        0 if ok else 1, True, ok, "" if ok else f"build={ok_b} seam={ok_s} harness={ok_h}"))
    else:
        results.append((len(results) + 1, "WIRING presence", "green", 0, True, True,
                        "SKIPPED (declared): a wiring surface is not on disk here — not a pass, not a fail"))

    # ---- THE TABLE ------------------------------------------------------------------------------
    shutil.rmtree(tmp_root, ignore_errors=True)
    print("=" * 100)
    print("_validate_polarities.py --selftest — every arm drives gate() on a copy of the REAL rows")
    print("=" * 100)
    print(f"{'#':>3}  {'result':6}  {'expect':6}  {'rc':>4}  {'named':5}  arm")
    fails = 0
    for n, name, expect, rc, named, ok, note in results:
        if not ok:
            fails += 1
        print(f"{n:>3}  {'PASS' if ok else 'FAIL':6}  {expect:6}  {str(rc):>4}  {('yes' if named else '-'):5}  {name}")
        if note and (not ok or note.startswith("SKIPPED")):
            print("        " + note.replace("\n", "\n        "))
    red_arms = [r for r in results if r[2] == "red"]
    red_ok = [r for r in red_arms if r[5]]
    green_arms = [r for r in results if r[2] == "green"]
    print("-" * 100)
    print(f"arms {len(results)} · red arms {len(red_arms)} (went red by name {len(red_ok)}/{len(red_arms)}) · "
          f"green arms {len(green_arms)} · no-fire/77 arms {len(results) - len(red_arms) - len(green_arms)} · "
          f"failures {fails}")
    if fails:
        print(f"✗ selftest FAILED — {fails} arm(s)")
        return 1
    print("✓ selftest OK — control green; every refusal arm red by its name; nothing written on refusal")
    return 0


# ============================================================================================
# ARGV — a contract, not a membership test (#208 class): unknown tokens refuse, rc 2
# ============================================================================================
FLAGS = {"--check": 0, "--write": 0, "--selftest": 0, "--dry-run": 0,
         "--add-polarity": 1, "--add-stub": 1, "--brain": 1}
USAGE = ("usage: --check | --write | --selftest | --add-polarity FILE [--dry-run|--write] | "
         "--add-stub FILE [--dry-run|--write]   [--brain DIR]")


def main(argv):
    if not argv:
        print(f"⛔ REFUSED (argv) — no arguments: this script writes files under --write and refuses to "
              f"guess. {USAGE}", file=sys.stderr)
        return 2
    opts, i = {}, 0
    while i < len(argv):
        tok = argv[i]
        if tok not in FLAGS:
            print(f"⛔ REFUSED (argv) — unknown argument {tok!r}. {USAGE}", file=sys.stderr)
            return 2
        if FLAGS[tok]:
            if i + 1 >= len(argv):
                print(f"⛔ REFUSED (argv) — {tok} needs a value. {USAGE}", file=sys.stderr)
                return 2
            opts[tok] = argv[i + 1]
            i += 2
        else:
            opts[tok] = True
            i += 1
    brain = opts.get("--brain") or os.environ.get("POLARITY_BRAIN_DIR") or DEFAULT_BRAIN
    brain = os.path.abspath(brain)
    if "--selftest" in opts:
        return selftest(brain)
    if "--add-polarity" in opts or "--add-stub" in opts:
        which = "polarity" if "--add-polarity" in opts else "stub"
        src = opts.get("--add-polarity") or opts.get("--add-stub")
        if "--write" not in opts and "--dry-run" not in opts:
            print("⛔ REFUSED (argv) — --add-* needs --dry-run or --write, stated.", file=sys.stderr)
            return 2
        try:
            entry = json.loads(read_text(src))
        except Exception as e:
            print(f"⛔ REFUSED (S-PARSE) — {src}: {e}", file=sys.stderr)
            return 2
        return add_entry(brain, which, entry, write="--write" in opts)
    if "--write" in opts:
        return gate(brain, write=True)
    if "--check" in opts:
        return gate(brain, write=False)
    print(f"⛔ REFUSED (argv) — nothing to do. {USAGE}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
