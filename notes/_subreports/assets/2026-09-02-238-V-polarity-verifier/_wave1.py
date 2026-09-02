#!/usr/bin/env python3
"""WAVE 1 — the brief's hostile rows (V brief item 2) + their obvious variants. All on copies."""
import json
import os
import re
import sys

sys.path.insert(0, "/sessions/wonderful-adoring-euler/mnt/outputs/v238")
from _v_attack import *  # noqa: E402,F401,F403

GEN = "_generated"


def rewrite(path, fn):
    t = open(path, encoding="utf-8").read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(fn(t))


# ---- 1. ref that resolves only case-insensitively --------------------------------------------
arm(10, "ref-case-party-pr-Fitts", "red",
    pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pr-Fitts", "role": "side_c"})),
    "R1-DANGLING", basis="s238-D7 (1): a party id that does not resolve; the register key is pr-fitts")
arm(11, "ref-case-link-S116-D1", "red",
    pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "S116-D1"})),
    "R1-DANGLING", basis="s238-D7 (1): a link id that does not resolve; the store key is s116-D1")
arm(12, "ref-case-link-s116-d1-lower", "red",
    pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "s116-d1"})),
    "R1-DANGLING", basis="s238-D7 (1)")

# ---- 2. stub whose phrase is empty -----------------------------------------------------------
arm(20, "stub-phrase-empty", "red",
    stubs(lambda o: o["stubs"].append({"id": "st-empty", "phrase": ""})),
    "S-STUB-SHAPE", basis="brief: a stub is an id + the verbatim phrase")
arm(21, "stub-phrase-whitespace-only", "red",
    stubs(lambda o: o["stubs"].append({"id": "st-blank", "phrase": "   "})),
    "S-STUB-SHAPE", basis="brief: a stub is an id + the verbatim phrase")
arm(22, "stub-phrase-zero-width-space-only", "red",
    stubs(lambda o: o["stubs"].append({"id": "st-zwsp", "phrase": "​"})),
    "S-STUB-SHAPE", basis="a phrase of one zero-width space is visually empty; str.strip() does not strip U+200B",
    note="EDGE: an effectively empty phrase")

# ---- 3. links[].ref to a _rulings.json id whose status is not `ruled` ------------------------
arm(30, "link-to-s200-D2-superseded-in-prose", "red",
    pol(lambda o: o["polarities"][2]["links"].append({"type": "resolvedBy", "ref": "s200-D2"})),
    "R1-SUPERSEDED", basis="s200-D3's status says 'supersedes s200-D2's theme scope' — but s200-D2 carries no superseded_by field; the gate reads only that field",
    note="store-vocabulary escape: supersession lives in prose for 4 of 5 supersessions")
arm(31, "link-resolvedBy-gauge-band-status-open", "red",
    pol(lambda o: o["polarities"][2]["links"].append({"type": "resolvedBy", "ref": "gauge-band"})),
    "R1-DANGLING", basis="'gauge-band' status: 'retire-or-pin FORKED TO DAVE and still open' — a resolvedBy to an OPEN item derives `resolved`",
    note="the derived status would flip pl-03 open -> resolved on an item the store calls open")
arm(32, "link-resolvedBy-s182-D1-PARKED", "red",
    pol(lambda o: o["polarities"][2]["links"].append({"type": "resolvedBy", "ref": "s182-D1"})),
    "R1-DANGLING", basis="s182-D1 status contains PARKED; s238-D3: status derived from the store — a parked ruling resolving a polarity")

# ---- 4. party role outside any vocabulary ----------------------------------------------------
arm(40, "role-SIDE_A-uppercase", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", "SIDE_A")), "S-ROLE", basis="schema enum")
arm(41, "role-trailing-space", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", "side_a ")), "S-ROLE", basis="schema enum")
arm(42, "role-null", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", None)), "S-ROLE", basis="schema type string + enum",
    note="expect S-ROLE or S-SCHEMA; a null role is outside every vocabulary")
arm(43, "role-missing-key", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__delitem__("role")), "S-SCHEMA", basis="schema required")
arm(44, "role-object-unhashable", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", {"side": "a"})), "S-SCHEMA",
    basis="schema type string", note="code: roles = {p.get('role') ...} hashes the value BEFORE the schema verdict is read")

# ---- 5. the same principle twice under different roles ---------------------------------------
arm(50, "same-principle-twice-different-roles", "red",
    pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pr-jakobs-law", "role": "side_c"})),
    "S-DUP-PARTY", basis="schema description: the same ref may not appear twice on one node")
arm(51, "same-principle-both-sides-a-and-b", "red",
    pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pr-jakobs-law", "role": "side_b"})),
    "S-DUP-PARTY", basis="a principle pulling against itself is not a polarity (s238-D4)")

# ---- 6. generated file hand-edited, LENGTH PRESERVED ------------------------------------------
def gen_flip_case(d):
    p = os.path.join(d, GEN, "polarity-status.json")
    rewrite(p, lambda t: t.replace('"status_derived": "open"', '"status_derived": "oPen"', 1))
arm(60, "gen-status-hand-edit-same-length", "red", gen_flip_case, "R4-AUTHORED-GENERATED", decisive="as-is",
    basis="s238-D7 (4) content-freshness; length preserved (open -> oPen)")


def gen_flip_case_resha(d):
    p = os.path.join(d, GEN, "polarity-status.json")
    obj = json.loads(open(p, encoding="utf-8").read())
    obj["rows"][0]["status_derived"] = "oPen" if obj["rows"][0]["status_derived"] == "open" else obj["rows"][0]["status_derived"].upper()
    import hashlib
    body = {k: v for k, v in obj.items() if k not in ("$header", "generated_at", "content_sha256")}
    obj["content_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
arm(61, "gen-status-hand-edit-with-recomputed-sha", "red", gen_flip_case_resha, "STALE-GENERATED", decisive="as-is",
    basis="a hand-editor who recomputes the self-sha must still be caught by the re-derivation at the on-disk clock")


def edges_hand_edit_same_length(d):
    p = os.path.join(d, GEN, "polarity-edges.json")
    rewrite(p, lambda t: t.replace('"from": "pr-', '"from": "PR-', 1))
arm(62, "gen-edges-hand-edit-same-length", "red", edges_hand_edit_same_length, "R4-AUTHORED-GENERATED", decisive="as-is",
    basis="s238-D7 (4)")


def txt_hand_edit_same_length(d):
    p = os.path.join(d, GEN, "defaults-declaration.txt")
    rewrite(p, lambda t: t.replace("declared: 0", "declared: 9", 1))
arm(63, "gen-txt-hand-edit-same-length", "red", txt_hand_edit_same_length, "R4-AUTHORED-GENERATED", decisive="as-is",
    basis="s238-D5: the declaration is derived; 'declared: 0' -> 'declared: 9' by hand")

# ---- 7. generated_at in the future / not a clock at all ---------------------------------------
def future_clock(d):
    for n in ("polarity-status.json", "polarity-edges.json"):
        rewrite(os.path.join(d, GEN, n), lambda t: t.replace('"generated_at": "2026-09-02T', '"generated_at": "2099-01-01T', 1))
    rewrite(os.path.join(d, GEN, "defaults-declaration.txt"), lambda t: t.replace("generated_at: 2026-09-02T", "generated_at: 2099-01-01T", 1))
arm(70, "gen-generated_at-in-the-future", "red", future_clock, None, decisive="as-is",
    basis="s238-D3: derived WITH A CLOCK; a clock in 2099 on a file whose body was derived today is a hand edit",
    note="the sha excludes generated_at; --check re-derives AT the on-disk clock, so any clock string is its own oracle")


def garbage_clock(d):
    rewrite(os.path.join(d, GEN, "polarity-status.json"), lambda t: t.replace('"generated_at": "2026-09-02T15:18:55Z"', '"generated_at": "banana"', 1))
arm(71, "gen-generated_at-is-banana", "red", garbage_clock, None, decisive="as-is",
    basis="s238-D3: a clock; 'banana' is not a clock", note="no shape check on generated_at")


def header_only_edit(d):
    rewrite(os.path.join(d, GEN, "polarity-status.json"), lambda t: t.replace("do not hand-edit", "do not hand-edit!", 1))
arm(72, "gen-header-text-edited", "red", header_only_edit, "R4-AUTHORED-GENERATED", decisive="as-is", basis="s238-D7 (4)")

# ---- 8. additionalProperties smuggle via a nested object -------------------------------------
arm(80, "smuggle-note-as-object", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", {"text": "aesthetics wins, always", "why": "because"})),
    "S-SCHEMA", basis="schema note: type string", note="expect a schema type refusal; the NAME is S-SCHEMA not R3")
arm(81, "smuggle-sources-item-extra-key", "red",
    pol(lambda o: o["polarities"][0]["sources"][0].__setitem__("judgement", "Jakob wins in Apollo, Von Restorff loses")),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3): a judgement text field of ANY name on a node — sources[] is on the node")
arm(82, "smuggle-top-level-$migration-nested-verdicts", "red",
    pol(lambda o: o["$migration"].__setitem__("verdicts", {"pl-01": "Jakob wins in Apollo — Von Restorff only for the one primary action per screen, never for chrome."})),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3): the node's only judgement is a typed link; a per-node verdict map under $migration is a judgement field by another door",
    note="$migration / $description are allowed top-level keys with UNVALIDATED content")
arm(83, "smuggle-top-level-$description-replaced-by-500-words", "red",
    pol(lambda o: o.__setitem__("$description", " ".join(["Aesthetics must win over usability in every Apollo review page because Dave rules by eye."] * 32))),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3)", note="$description is free text of any length")
arm(84, "smuggle-4th-top-level-key-$notes", "red",
    pol(lambda o: o.__setitem__("$notes", {"pl-01": "Jakob wins"})), "R3-JUDGEMENT-FIELD", basis="s238-D7 (3)")
arm(85, "smuggle-link-extra-key-reason", "red",
    pol(lambda o: o["polarities"][0]["links"][0].__setitem__("reason", "because the law is a budget and budgets win")),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3)")

# ---- 9. unicode-confusable ids ----------------------------------------------------------------
arm(90, "confusable-party-ref-cyrillic-s", "red",
    pol(lambda o: o["polarities"][27]["parties"].append({"ref": "pr-information-sсent", "role": "side_c"})),
    "S-ID", basis="brief: pr-information-scent vs Cyrillic с")
arm(91, "confusable-link-ref-cyrillic-s116", "red",
    pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "ѕ116-D1"})),
    "S-ID", basis="link ref with Cyrillic ѕ; the R1 loop `continue`s on non-ASCII and relies on the schema pattern walk")
arm(92, "confusable-stub-id-cyrillic", "red",
    stubs(lambda o: o["stubs"].append({"id": "st-brand-pаlette", "phrase": "brand palette (again)"})),
    "S-STUB-SHAPE", basis="STUB_ID pattern is ASCII")
arm(93, "confusable-sources-id-breaks-the-oracle", "red",
    pol(lambda o: o["polarities"][0]["sources"][0].__setitem__("id", "tn-0１")),
    None, basis="R3-QUOTE-NOT-VERBATIM depends on the source row being reachable; a confusable sources[].id makes every quote on the node UNVERIFIED — declared, then PASSED",
    note="quote-laundering by breaking the node's own source pointer")

# ---- 10. a 31st row appended without a stub ---------------------------------------------------
NEW31 = {"id": "pl-31", "parties": [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}],
         "mediating_variable": "target count", "links": [], "sources": [{"path": "notes/nowhere.json", "id": "tn-31"}]}
arm(100, "row31-no-stub-fictional-source", "green",
    pol(lambda o: o["polarities"].append(dict(NEW31))), None,
    basis="legal by the schema: sources[].path is never checked for existence; a 31st row with a fictional receipt is accepted",
    note="green by the letter; the receipt is unverified")
arm(101, "row31-party-is-a-phrase-not-a-stub", "red",
    pol(lambda o: o["polarities"].append(dict(NEW31, id="pl-32", parties=[{"ref": "pr-fitts", "role": "side_a"}, {"ref": "dense-financial-tables", "role": "side_b"}]))),
    "R1-DANGLING", basis="s238-D7 (1)")
arm(102, "row31-party-is-an-undeclared-st", "red",
    pol(lambda o: o["polarities"].append(dict(NEW31, id="pl-33", parties=[{"ref": "pr-fitts", "role": "side_a"}, {"ref": "st-not-declared-anywhere", "role": "side_b"}]))),
    "R1-UNDECLARED-STUB", basis="s238-D7 (1)")
arm(103, "row31-id-one-digit-pl-1", "red",
    pol(lambda o: o["polarities"].append(dict(NEW31, id="pl-1"))), "S-ID", basis="schema pattern ^pl-[0-9]{2,}$")
arm(104, "row31-duplicates-pl-01-id", "red",
    pol(lambda o: o["polarities"].append(dict(NEW31, id="pl-01"))), "S-DUP-ID", basis="P arm 34 variant: a different body under an existing id")

# ---- 11. the schema file itself mutated -------------------------------------------------------
def schema_minitems_1_plus_one_party_row(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["parties"].__setitem__("minItems", 1))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0].__setitem__("parties", o["polarities"][0]["parties"][:1]))
arm(110, "schema-minItems-2-to-1-plus-one-party-row", "red", schema_minitems_1_plus_one_party_row, "S-MIN-PARTIES",
    basis="the brief's row; s238-D4 a polarity is a pull between TWO true things; P arm 49 calls this no-fire by design",
    note="the schema is an unguarded loosening surface: no sha pin, no floor in code")


def schema_fifth_type_plus_row(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["links"]["items"]["properties"]["type"]["enum"].append("relatedTo"))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0]["links"].append({"type": "relatedTo", "ref": "s116-D1"}))
arm(111, "schema-enum-widened-fifth-type-relatedTo", "red", schema_fifth_type_plus_row, "R2-UNKNOWN-TYPE",
    basis="s238-D6: four types; 'a fifth link type is NOT ruled' (P brief DO NOT RULE) — the schema admits one by edit")


def schema_party_additional_true_plus_why(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["parties"]["items"].__setitem__("additionalProperties", True))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0]["parties"][0].__setitem__("why", "because Jakob wins in Apollo"))
arm(112, "schema-party-additionalProperties-true-plus-why", "red", schema_party_additional_true_plus_why, "R3-JUDGEMENT-FIELD",
    basis="s238-D7 (3): a judgement field inside a party; the schema's `false` is the only thing refusing it")


def schema_node_additional_true_plus_verdict(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s.__setitem__("additionalProperties", True))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0].__setitem__("verdict", "Jakob wins"))
arm(113, "schema-node-additionalProperties-true-plus-verdict", "red", schema_node_additional_true_plus_verdict, "R3-JUDGEMENT-FIELD",
    basis="s238-D7 (3) at node level — here the code has its own check independent of the schema")


def schema_maxwords_raised(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["links"]["items"]["properties"]["quote"].__setitem__("maxWords", 150))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0]["links"][0].__setitem__("quote", "The law IS a Von Restorff budget with a legal contrast floor attached. " * 3))
arm(114, "schema-quote-maxWords-raised-to-150", "red", schema_maxwords_raised, "R3-QUOTE-TOO-LONG",
    basis="s238-D7 (3): the 15-word bound lives only in the schema; a 39-word verbatim quote passes once the bound is raised",
    note="the quote is verbatim-checked so it must still be a substring; the 3x repeat is NOT a substring — expect R3-QUOTE-NOT-VERBATIM instead if maxWords is bypassed")

# ---- 12. an empty links array — legal or not? ---------------------------------------------------
arm(120, "links-empty-array", "green",
    pol(lambda o: o["polarities"][0].__setitem__("links", [])), None,
    basis="s238-D6 refuses an UNTYPED link, not an absent one; s238-D7 (3) permits zero links; 18 real rows already carry links: []")
arm(121, "links-key-missing", "red",
    pol(lambda o: o["polarities"][0].__delitem__("links")), "S-SCHEMA", basis="schema required: links")

print(table())
dump("/sessions/wonderful-adoring-euler/mnt/outputs/v238/logs/wave1.json")
