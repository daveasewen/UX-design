#!/usr/bin/env python3
"""WAVE 2 — lane V's own hostile rows: the closed directory's edges, the free-text fields refusal 3
does not reach, the oracle the quote check trusts, crashes that are not refusals, the register."""
import json
import os
import sys

sys.path.insert(0, "/sessions/wonderful-adoring-euler/mnt/outputs/v238")
from _v_attack import *  # noqa: E402,F401,F403

GEN = "_generated"
ZW = "​"


def wfile(path, text, mode="w", enc="utf-8"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if "b" in mode:
        with open(path, mode) as f:
            f.write(text)
    else:
        with open(path, mode, encoding=enc) as f:
            f.write(text)


# ---- A. untyped links that are not a dict-without-type --------------------------------------
arm(200, "link-bare-string", "red", pol(lambda o: o["polarities"][0]["links"].append("s116-D1")), "R2-UNTYPED",
    basis="s238-D6: an untyped link refused — a bare id IS the most natural untyped link")
arm(201, "link-type-null", "red", pol(lambda o: o["polarities"][0]["links"].append({"type": None, "ref": "s116-D1"})), "R2-UNTYPED",
    basis="s238-D6")
arm(202, "link-type-is-a-list", "red", pol(lambda o: o["polarities"][0]["links"].append({"type": ["touches"], "ref": "s116-D1"})), "R2-UNKNOWN-TYPE",
    basis="s238-D6", note="code: key = (l.get('type'), ref) is hashed for the duplicate check before the schema verdict is read")
arm(203, "party-ref-is-a-list", "red", pol(lambda o: o["polarities"][0]["parties"].append({"ref": ["pr-fitts"], "role": "side_c"})), "S-SCHEMA",
    basis="schema type string", note="code: party_refs = {p.get('ref') ...} hashes the value")
arm(204, "stub-id-is-a-list", "red", stubs(lambda o: o["stubs"].append({"id": ["st-x"], "phrase": "x"})), "S-STUB-SHAPE",
    basis="a stub id must match the pattern", note="code: s.get('id') in seen_ids hashes the value")

# ---- B. the closed directory's edges ----------------------------------------------------------
arm(210, "hidden-dotfile-edges-at-brain-top", "red",
    lambda d: wfile(os.path.join(d, ".edges.json"), json.dumps({"edges": [{"from": "pr-fitts", "to": "pr-hick", "polarity": "pl-99"}]}) + "\n"),
    "R4-AUTHORED-EDGES", decisive="as-is", basis="s238-D7 (4): an authored edge file; check_home_dir skips names starting with '.'")
arm(211, "hidden-dotfile-inside-_generated", "red",
    lambda d: wfile(os.path.join(d, GEN, ".authored-edges.json"), json.dumps({"edges": []}) + "\n"),
    "R4-STRAY-FILE", decisive="as-is", basis="s238-D7 (4): nothing under the generated path may be authored; dotfiles are skipped")
arm(212, "leftover-tmp-inside-_generated", "red",
    lambda d: wfile(os.path.join(d, GEN, ".polarity-edges.json.tmp"), "{\"edges\": [1]}\n"),
    "R4-STRAY-FILE", decisive="as-is", basis="a half-written .tmp from an interrupted --write survives every door")
arm(213, "authored-edges-under-schema-dir", "red",
    lambda d: wfile(os.path.join(d, "schema", "edges.json"), json.dumps({"edges": [{"from": "pr-fitts", "to": "pr-hick"}]}) + "\n"),
    "R4-AUTHORED-EDGES", decisive="as-is", basis="s238-D7 (4) / s238-D1: schema/ is in ALLOWED_TOP but its CONTENTS are never listed")
arm(214, "second-schema-under-schema-dir", "red",
    lambda d: wfile(os.path.join(d, "schema", "polarity.schema.v2.json"), "{\"minItems\": 1}\n"),
    "R4-STRAY-FILE", decisive="as-is", basis="s238-D1: a second stored shape; schema/ is unlisted")
arm(215, "subdir-edges-at-brain-top", "red",
    lambda d: wfile(os.path.join(d, "edges", "authored.json"), json.dumps({"edges": []}) + "\n"),
    "R4-STRAY-FILE", decisive="as-is", basis="a directory is not in ALLOWED_TOP")
arm(216, "pycache-dir-carrying-edges", "red",
    lambda d: wfile(os.path.join(d, "__pycache__", "edges.json"), json.dumps({"edges": []}) + "\n"),
    "R4-STRAY-FILE", decisive="as-is", basis="__pycache__ is skipped by name")
arm(217, "generated-dir-is-a-file", "red",
    lambda d: (shutil.move(os.path.join(d, GEN), os.path.join(d, ".gen-moved")), wfile(os.path.join(d, GEN), "authored\n")),
    "MISSING-GENERATED", decisive="as-is", basis="control: the derived path replaced by a file")

# ---- C. the oracle the quote check trusts -------------------------------------------------------
arm(220, "quote-oracle-repointed-to-_rulings.json", "red",
    pol(lambda o: (o["polarities"][0].__setitem__("sources", [{"path": "knowledge/_rulings.json", "id": "s238-D7"}]),
                   o["polarities"][0]["links"][0].__setitem__("quote", "A gate that is not a consumer of every commit is not a gate"))),
    "R3-QUOTE-NOT-VERBATIM", basis="s238-D7 (3): the quote must justify the TYPE from the node's source row; the node names its own oracle",
    note="the quote is verbatim — from s238-D7's text, not from tn-01")
arm(221, "quote-oracle-repointed-to-itself", "red",
    pol(lambda o: (o["polarities"][0].__setitem__("sources", [{"path": "knowledge/brain/polarities.json", "id": "pl-01"}]),
                   o["polarities"][0]["links"][0].__setitem__("quote", o["polarities"][0]["mediating_variable"]))),
    "R3-QUOTE-NOT-VERBATIM", basis="the node is its own source row; the quote is its own mediating_variable")
arm(222, "quote-paraphrased-AND-source-pointer-broken", "red",
    pol(lambda o: (o["polarities"][0]["sources"][0].__setitem__("path", "notes/no-such-file.json"),
                   o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget"))),
    "R3-QUOTE-NOT-VERBATIM", basis="P arm 23's paraphrase, plus a broken pointer: the paraphrase is now UNVERIFIED and passes")
arm(223, "quote-empty-string", "red",
    pol(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1", "quote": ""})),
    "R3-QUOTE-NOT-VERBATIM", basis="'' is a substring of everything; an empty receipt justifies a resolvedBy that closes pl-01",
    note="also moves the sort: pl-01 open -> resolved")
arm(224, "quote-one-word-the", "red",
    pol(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1", "quote": "the"})),
    "R3-QUOTE-NOT-VERBATIM", basis="a one-word verbatim 'receipt' closes pl-01 as resolved")
arm(225, "sources-path-absolute-outside-repo", "green",
    pol(lambda o: o["polarities"][0]["sources"].append({"path": "/etc/hostname", "id": "x"})), None,
    basis="observation: sources[].path is joined with os.path.join(REPO, path) — an absolute path escapes the repo; accepted")

# ---- D. the free-text fields refusal 3 does not reach --------------------------------------------
arm(230, "note-is-a-14-word-judgement", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", "Jakob must always win in Apollo because Dave rules by eye and prefers familiarity")),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3): a judgement text field of any name; the schema calls note 'a verbatim gloss' but nothing checks verbatim-ness — only word count")
arm(231, "note-40-words-joined-by-zero-width-spaces", "red",
    pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", ZW.join(["Jakob", "must", "always", "win", "in", "Apollo", "because", "Dave", "rules", "by", "eye"] * 4))),
    "R3-NOTE-TOO-LONG", basis="maxWords counts str.split() tokens; U+200B is not whitespace, so 44 visible words count as 1")
arm(232, "mediating_variable-300-word-judgement", "red",
    pol(lambda o: o["polarities"][0].__setitem__("mediating_variable", " ".join(["Jakob wins and Von Restorff loses in every Apollo review because familiarity outranks salience."] * 20))),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3): mediating_variable has minLength 1 and NO maxWords — an unbounded free-text field on the node")
arm(233, "sources-id-300-word-judgement", "red",
    pol(lambda o: o["polarities"][3]["sources"][0].__setitem__("id", " ".join(["aesthetics wins over usability in Apollo, always, by Dave's eye."] * 30))),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3): sources[].id has minLength 1 and no bound; pl-04 has no quotes so nothing is even UNVERIFIED")
arm(234, "stub-phrase-15-word-judgement", "red",
    stubs(lambda o: o["stubs"].append({"id": "st-dense-tables-win", "phrase": "dense financial tables must always beat whitespace in Apollo because Dave prefers density everywhere"})),
    "R3-JUDGEMENT-FIELD", basis="s238-D7 (3) by another door: a stub 'phrase' is meant to be a verbatim T-finding-8 phrase; nothing checks it; 15 words of verdict declared as a party")
arm(235, "orphan-stub-declared-never-used", "green",
    stubs(lambda o: o["stubs"].append({"id": "st-orphan-phrase", "phrase": "an orphan phrase"})), None,
    basis="observation: a declared stub no polarity references passes every door and is not even STALE (stubs are not in any derived file)")

# ---- E. the register and the store ---------------------------------------------------------------
def demote_obligation(d):
    o = json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())
    p = json.loads(open(os.path.join(d, "principles.json"), encoding="utf-8").read())
    reg = {x["id"]: x for x in p["principles"]}
    # pl-15's obligation party: the first party on any node whose grade is L
    target = None
    for n in o["polarities"]:
        for pt in n["parties"]:
            if pt["ref"] in reg and reg[pt["ref"]].get("grade") == "L":
                target = (n["id"], pt["ref"]); break
        if target: break
    reg[target[1]]["grade"] = "C"
    with open(os.path.join(d, "principles.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(p, indent=1, ensure_ascii=False) + "\n")
    with open(os.path.join(d, "DEMOTED.txt"), "w") as f:
        f.write(f"{target}\n")
    os.remove(os.path.join(d, "DEMOTED.txt"))
arm(240, "register-obligation-demoted-L-to-C", "red", demote_obligation, None,
    basis="s237-D2: obligation outranks; s238-D1: principles.json is the register — a grade letter edit silently re-sorts a settled-by-obligation row; no receipt against R1's seed",
    note="expect: accepted after --write; the sort moves 6·4·20 -> 5·x·x with no refusal")
arm(241, "register-statement-rewritten", "red",
    principles(lambda p: p["principles"][0].__setitem__("statement", "Fitts is wrong and Apollo ignores it.")), None,
    basis="P report: 'seeded ONCE byte-for-byte, no edits' — the gate holds no sha against the seed; a statement rewrite passes")
arm(242, "register-principle-removed-that-is-a-party", "red",
    principles(lambda p: p["principles"].__delitem__(next(i for i, x in enumerate(p["principles"]) if x["id"] == "pr-jakobs-law"))),
    "R1-DANGLING", basis="control: s238-D7 (1)")
arm(243, "same-ruling-resolvedBy-AND-challengedBy", "red",
    pol(lambda o: o["polarities"][15]["links"].append({"type": "challengedBy", "ref": "s116-D1"})), None,
    basis="pl-16 already carries resolvedBy s116-D1; the same ruling both resolves and is challenged by the node — a contradiction the gate does not refuse (unruled; observation)")
arm(244, "all-30-rows-deleted", "red", pol(lambda o: o.__setitem__("polarities", [])), None,
    basis="observation: the migration receipt ($migration) is decorative; 0 rows passes after --write; no floor on the row count")
arm(245, "all-21-links-deleted", "red", pol(lambda o: [n.__setitem__("links", []) for n in o["polarities"]]), None,
    basis="observation: the 21 typed links (s238-D6's migration) can be wiped; sort becomes 6·0·24; no refusal")
arm(246, "$migration-sha256-garbage", "red",
    pol(lambda o: o["$migration"].__setitem__("sha256", "0" * 64)), None,
    basis="the $migration.sha256 receipt is never verified by the gate — decorative")
arm(247, "$migration-from-nonexistent", "red",
    pol(lambda o: o["$migration"].__setitem__("from", "notes/does-not-exist.json")), None, basis="same")
arm(248, "node-all-parties-are-stubs", "green",
    pol(lambda o: o["polarities"].append({"id": "pl-40", "parties": [{"ref": "st-brand-palette", "role": "side_a"}, {"ref": "st-consistency-of-investment-across-a-journey", "role": "side_b"}],
                                          "mediating_variable": "x", "links": [], "sources": [{"path": "x", "id": "y"}]})), None,
    basis="s238-D1: a declared stub is a legal party — a polarity between two phrases with no register node at either end is legal; observation")

# ---- F. crashes that are not refusals -------------------------------------------------------------
arm(250, "sources-item-without-path-plus-a-quote", "red",
    pol(lambda o: o["polarities"][0].__setitem__("sources", [{"id": "tn-01"}])), "S-SCHEMA",
    basis="schema required path", note="code: _source_row_text(None, ...) -> os.path.join(REPO, None)")
arm(251, "sources-path-is-an-int", "red",
    pol(lambda o: o["polarities"][0]["sources"][0].__setitem__("path", 5)), "S-SCHEMA", basis="schema type string")
arm(252, "polarities.json-invalid-utf8-byte", "red",
    lambda d: wfile(os.path.join(d, "polarities.json"), open(os.path.join(d, "polarities.json"), "rb").read().replace(b"pr-jakobs-law", b"pr-jakobs-l\xe1w", 1), mode="wb"),
    "S-PARSE", basis="parse in the consumer's grammar: a byte that is not UTF-8 must be a NAMED parse refusal")
arm(253, "polarities.json-utf8-bom", "red",
    lambda d: wfile(os.path.join(d, "polarities.json"), b"\xef\xbb\xbf" + open(os.path.join(d, "polarities.json"), "rb").read(), mode="wb"),
    "S-PARSE", basis="control")
arm(254, "stubs.json-is-a-list", "red", lambda d: wfile(os.path.join(d, "stubs.json"), "[]\n"), "S-SHAPE", basis="control")
arm(255, "principles-list-is-a-dict", "red", principles(lambda p: p.__setitem__("principles", {})), "S-SHAPE", basis="control")
arm(256, "schema-properties-is-a-list", "red", schema(lambda s: s.__setitem__("properties", [])), "S-SCHEMA",
    basis="a mutated schema must refuse by name, not crash", note="code: for pk, pv in v.items()")
arm(257, "schema-pattern-invalid-regex", "red", schema(lambda s: s["properties"]["id"].__setitem__("pattern", "^pl-[")), "S-SCHEMA",
    basis="a mutated schema must refuse by name, not crash")
arm(258, "schema-type-is-a-list", "red", schema(lambda s: s["properties"]["parties"]["items"]["properties"]["note"].__setitem__("type", ["string", "null"])), "S-SCHEMA",
    basis="draft 2020-12 allows a type list; this reader does not — must refuse loudly")

print(table())
dump("/sessions/wonderful-adoring-euler/mnt/outputs/v238/logs/wave2.json")
