#!/usr/bin/env python3
"""_validate_roles_resolve.py — the ROLE/ANSWERS ADDRESS-RESOLVE check (#253, lane C).

WHAT THIS IS. The 25-meta pass (s251-D12) puts eight interchangeability terms on the
component metas — `provides · answers · shape · span · priority · when · with · not-with`
(the DESK eight, s251-D3…D8). Four of them are ADDRESSES into a store that is the ONE
home for its vocabulary (ADR-0017 write-once):
  * `provides`      -> knowledge/roles.json `roles`      (the twelve slugs, s252-D1)
  * `answers`       -> knowledge/chart-intents.json      (extended to non-charts, s251-D11)
  * `not-with[].slug` -> a meta stem OR a role slug      (s251-D6, slug REQUIRED)
  * `with[].slug`     -> a meta stem OR a role slug      (s251-D6, normally on the ROLE)
This script is those addresses' FIRST AND ONLY resolver — the reader that makes the fields
a lookup rather than prose with extra syntax. It is the sibling of
_validate_intent_resolve.py (#195) and is written on that file's pattern deliberately.

WHY IT LANDS IN THE SAME CHANGE AS THE FIELDS. An address nothing resolves is the #145
binds gap and the [[instrument-without-a-consumer]] class: it LOOKS checked and is not,
which is worse than a copy. The premise probe for #253 found NO consumer of
`provides/shape/span/...` anywhere in the repo — this validator IS the first consumer,
and it lands with the schema, before lanes A and B author a single value.

THE CHECKS (each named in the output; by addition only — this script NEVER edits):
  1  provides-resolves   every `provides` is a key of `roles` in roles.json.
  2  answers-resolves    every `answers` word is a key of `chart-intent` in
                         chart-intents.json. An unknown word REFUSES, loud and NAMED —
                         it is never silently added; a new word enters the store only by
                         Dave's ruling (s251-D11: ONE closed list, ONE resolver).
  3  notwith-resolves    every `not-with[].slug` resolves to a meta stem or a role slug.
  4  with-resolves       every `with[].slug` resolves to a meta stem or a role slug.
  5  priority-unique     `priority` is unique WITHIN A ROLE across the metas providing it
                         (it is an in-role ordering, update-alternatives; a tie makes the
                         ordering unreadable).
  6  priority-in-role    a `priority` with no `provides` is a number about nothing.
  7  intent-equals-answers  where a chart meta carries BOTH, the values must be EQUAL
                         (the #253 call: `answers` is the general field, `intent` is not
                         renamed and keeps its own resolver; two homes for one fact must
                         at least agree).
  8  span-ordered        `span.cols.min` <= `span.cols.max`. The 1..12 BOUNDS are the
                         schema's job (s251-D10, 12-col canon); draft-07 cannot compare
                         two siblings, so the ordering is checked here.
  9  shape-known         every `shape` is a key of `shapes` in knowledge/shapes.json.
                         s254-D2 item 1 CLOSED that vocabulary — page B's grammar
                         `<x-dimension> × <mark>` is the one grammar and the store is its
                         ONE home. Until #254 this field resolved against NOTHING; a new
                         value enters the store by Dave's ruling, never by a lane.
 10  when-fields-known   every LEFT-HAND field name in a `when` gate is a key of `fields`
                         in knowledge/when-fields.json. s251-D5 ruled `when` a PREDICATE
                         and deferred the field list; s254-D2 item 2 is that further
                         ruling. Parse: split the value on the FIRST em-dash and read only
                         the GATE half; a clause opening `<field> <operator>` is a field
                         claim, a clause with no operator is prose inside the gate and is
                         NOT parsed (the V-B operator-token method, M2). The per-field
                         COUNTS are printed so a review page quotes script output rather
                         than a human reading — that is what closes V-B's M2.

DERIVED, PRINTED, NEVER WRITTEN (s251-D6, Dave: "author one direction, the validator
derives the other"; ISO 25964 preferred-term/RT reciprocity):
  * `instead-of` GRADES. Co-providers of one role are substitutes for each other (FFF:
    same FUNCTION). The grade compares the other two FFF faces the metas carry — `shape`
    and `span` — and the ISO 25964 preferred term of the set is the highest `priority`.
    Grades: `equivalent` (shape equal AND span overlaps), `near` (one face matches),
    `distant` (neither). Direction is lower-priority -> preferred.
  * `not-with` RECIPROCALS. Exclusion is symmetric: A not-with B implies B not-with A.
  * `with` RECIPROCALS, marked WEAK — a complement is not symmetric in general (a
    Liskov-style one-way statement stays one-way, s251-D6), so the derived direction is
    printed as `suggests` and flagged for a human, never asserted.
These are PRINTED for a review page and for Dave's eye. Nothing is written back into any
meta. A derived reciprocal that a meta ALREADY declares is reported as `already-authored`,
not as a duplicate to add.

CROSS-CHECK, REPORT-ONLY BY RULING. roles.json's `providers` lists are the ADOPTED
MEMBERSHIP from the v1 review page; s252-D1 says the METAS become canon once the 25-meta
pass authors them, at which point this file's lists are "a cross-check, not a source".
So membership disagreement is REPORTED, never failed — and while ZERO metas carry
`provides` the report says so in as many words, so nobody reads an empty diff as agreement.

WHAT THIS CANNOT SEE, DECLARED.
  * It proves a word EXISTS in the vocabulary, not that it is the RIGHT word for that
    component. Correctness is Dave's eye, grounded in each meta's own `purpose` prose.
  * It checks that a `shape` value EXISTS in the store and that a `when` field name is
    legal. It does NOT check that the predicate is TRUE of the component, that the
    operators are used consistently, or that the prose half after the em-dash agrees with
    the gate half. It never parses the RIGHT-hand side of a clause: those value
    vocabularies (`present`/`absent`, `categorical`, counts) are NOT ruled.
  * Presence is not this check's business: a meta carrying none of the eight is skipped.
    No gate, no ratchet, no glob width is decided here.

Usage:  python3 knowledge/_validate_roles_resolve.py              # check mode
        python3 knowledge/_validate_roles_resolve.py --selftest   # 15 bites
        python3 knowledge/_validate_roles_resolve.py --mutate <name>
Exit non-zero on any failure. An ABSENT store or an EMPTY corpus glob fails LOUD — an
absent instrument must not read as a pass (_validate_binds_ratchet.py's rule).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import copy
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROLES = os.path.join(HERE, "roles.json")
INTENTS = os.path.join(HERE, "chart-intents.json")
SHAPES = os.path.join(HERE, "shapes.json")
WHENF = os.path.join(HERE, "when-fields.json")
COMP = os.path.join(HERE, "components")

TERMS = ("provides", "answers", "shape", "span", "priority", "when", "with", "not-with")

# s254-D2 item 2 — the `when` parse. GATE — PROSE, split on the FIRST em-dash; only the
# gate half is read. A clause opening `<field> <operator>` is a FIELD CLAIM; a clause with
# no operator is prose inside the gate and is NOT parsed (V-B's operator-token method, M2).
WHEN_OPS = ("!=", ">=", "<=", "==", "=", "≥", "≤", "<", ">", "in", "spans")
_WHEN_CLAUSE = re.compile(r"^([A-Za-z][A-Za-z0-9_.\-]*)\s*(%s)"
                          % "|".join(re.escape(o) if o.isalpha() is False else r"\b%s\b" % o
                                     for o in WHEN_OPS))


def when_field_claims(value):
    """Every (field, clause) a `when` gate CLAIMS. Prose clauses carry none, by design."""
    if not isinstance(value, str):
        return []
    gate = value.split("—")[0]
    out = []
    for clause in re.split(r"\bAND\b|\bOR\b", gate):
        m = _WHEN_CLAUSE.match(clause.strip())
        if m:
            out.append((m.group(1), clause.strip()))
    return out


# --------------------------------------------------------------------------- stores
def load_roles(path=ROLES):
    """The ONE home for the role vocabulary. Absent or malformed = LOUD failure."""
    if not os.path.exists(path):
        raise SystemExit("FAIL — roles store MISSING: %s (an absent instrument is "
                         "not a pass)" % path)
    data = json.loads(open(path, encoding="utf-8").read())
    roles = data.get("roles")
    if not isinstance(roles, dict) or not roles:
        raise SystemExit("FAIL — %s carries no non-empty `roles` object; the role "
                         "vocabulary has no home" % path)
    return roles


def load_answers(path=INTENTS):
    """The ONE home for the answers vocabulary (s251-D11 extends it to non-charts)."""
    if not os.path.exists(path):
        raise SystemExit("FAIL — answers store MISSING: %s (an absent instrument is "
                         "not a pass)" % path)
    data = json.loads(open(path, encoding="utf-8").read())
    vocab = data.get("chart-intent")
    if not isinstance(vocab, dict) or not vocab:
        raise SystemExit("FAIL — %s carries no non-empty `chart-intent` object; the "
                         "answers vocabulary has no home" % path)
    return vocab


def load_shapes(path=SHAPES):
    """The ONE home for the shape vocabulary (s254-D2 item 1). Absent = LOUD failure."""
    if not os.path.exists(path):
        raise SystemExit("FAIL — shape store MISSING: %s (an absent instrument is "
                         "not a pass)" % path)
    data = json.loads(open(path, encoding="utf-8").read())
    shapes = data.get("shapes")
    if not isinstance(shapes, dict) or not shapes:
        raise SystemExit("FAIL — %s carries no non-empty `shapes` object; the shape "
                         "vocabulary has no home" % path)
    return shapes


def load_when_fields(path=WHENF):
    """The ONE home for the `when` field list (s254-D2 item 2). Absent = LOUD failure."""
    if not os.path.exists(path):
        raise SystemExit("FAIL — when-field store MISSING: %s (an absent instrument is "
                         "not a pass)" % path)
    data = json.loads(open(path, encoding="utf-8").read())
    fields = data.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise SystemExit("FAIL — %s carries no non-empty `fields` object; the `when` "
                         "predicate's field list has no home" % path)
    return fields


def metas(comp_dir=COMP):
    return sorted(f for f in glob.glob(os.path.join(comp_dir, "*.meta.json"))
                  if not os.path.basename(f).startswith("EXAMPLE-"))


def stem(path):
    return os.path.basename(path)[:-len(".meta.json")]


def read_corpus(comp_dir=COMP):
    """Returns (docs, fails). A crash is not a fail — it is named and carried."""
    files = metas(comp_dir)
    if not files:
        raise SystemExit("FAIL — corpus glob matched ZERO metas under %s" % comp_dir)
    docs, fails = {}, []
    for f in files:
        try:
            docs[stem(f)] = json.loads(open(f, encoding="utf-8").read())
        except Exception as e:
            fails.append("%s: FAIL — unparseable JSON (%s)" % (os.path.basename(f), e))
    return docs, fails


# --------------------------------------------------------------------------- checks
def _words(val):
    """The hybrid shape the schema permits: a string, or a non-empty list of strings."""
    if isinstance(val, str):
        return [val], True
    if isinstance(val, list) and val and all(isinstance(w, str) for w in val):
        return list(val), True
    return [], False


def check(comp_dir=COMP, roles_path=ROLES, intents_path=INTENTS,
          shapes_path=SHAPES, when_path=WHENF):
    """Returns (fails, stats). Every offending value is NAMED with its file."""
    roles = load_roles(roles_path)
    vocab = load_answers(intents_path)
    shapes = load_shapes(shapes_path)
    whenf = load_when_fields(when_path)
    docs, fails = read_corpus(comp_dir)
    legal_roles = sorted(roles)
    legal_answers = sorted(vocab)
    legal_shapes = sorted(shapes)
    legal_when = sorted(whenf)
    known_slugs = set(docs) | set(roles)

    stats = {"metas": len(docs), "carrying": 0, "addresses": 0,
             "shape_values": {}, "when_fields": [], "by_role": {},
             "when_field_counts": {}, "when_prose_clauses": 0,
             "counts": {t: 0 for t in TERMS}}
    prio = {}   # role -> {priority -> [stem, ...]}

    for name in sorted(docs):
        d = docs[name]
        if not any(t in d for t in TERMS):
            continue
        stats["carrying"] += 1
        for t in TERMS:
            if t in d:
                stats["counts"][t] += 1

        # 1 provides-resolves
        role = None
        if "provides" in d:
            v = d["provides"]
            if not isinstance(v, str):
                fails.append("%s: FAIL [provides-resolves] — `provides` must be a single "
                             "role slug (string), got %r" % (name, v))
            else:
                stats["addresses"] += 1
                if v not in roles:
                    fails.append(
                        "%s: FAIL [provides-resolves] — UNKNOWN ROLE %r — not a key of "
                        "`roles` in knowledge/roles.json. Legal set: %s. The twelve roles "
                        "are ADOPTED (s252-D1), not invented: a thirteenth is Dave's "
                        "ruling, never a lane's drift." % (name, v, ", ".join(legal_roles)))
                else:
                    role = v
                    stats["by_role"].setdefault(v, []).append(name)

        # 2 answers-resolves
        if "answers" in d:
            words, ok = _words(d["answers"])
            if not ok:
                fails.append("%s: FAIL [answers-resolves] — `answers` must be a string or "
                             "a non-empty list of strings, got %r" % (name, d["answers"]))
            for w in words:
                stats["addresses"] += 1
                if w not in vocab:
                    fails.append(
                        "%s: FAIL [answers-resolves] — UNKNOWN ANSWER %r — not a key of "
                        "`chart-intent` in knowledge/chart-intents.json. Legal set: %s. "
                        "s251-D11 adopted ONE closed list and ONE resolver: a new word is "
                        "PROPOSED on a review page and added by Dave's ruling, NEVER "
                        "silently by a lane." % (name, w, ", ".join(legal_answers)))

        # 3/4 notwith-resolves, with-resolves
        for field, label in (("not-with", "notwith-resolves"), ("with", "with-resolves")):
            if field not in d:
                continue
            entries = d[field]
            if not isinstance(entries, list) or not entries:
                fails.append("%s: FAIL [%s] — `%s` must be a non-empty array of objects, "
                             "got %r" % (name, label, field, entries))
                continue
            for e in entries:
                if not isinstance(e, dict) or not isinstance(e.get("slug"), str):
                    fails.append("%s: FAIL [%s] — every `%s` entry needs a `slug` string "
                                 "(s251-D6: the slug is REQUIRED, no ref:null seat), "
                                 "got %r" % (name, label, field, e))
                    continue
                stats["addresses"] += 1
                if e["slug"] not in known_slugs:
                    fails.append(
                        "%s: FAIL [%s] — UNKNOWN SLUG %r in `%s` — resolves to neither a "
                        "meta stem under knowledge/components/ nor a role in "
                        "knowledge/roles.json." % (name, label, e["slug"], field))

        # 5/6 priority
        if "priority" in d:
            p = d["priority"]
            if not isinstance(p, int) or isinstance(p, bool):
                fails.append("%s: FAIL [priority-unique] — `priority` must be an integer, "
                             "got %r" % (name, p))
            elif role is None:
                fails.append(
                    "%s: FAIL [priority-in-role] — `priority` %r with no resolving "
                    "`provides`. Priority is compared ONLY within one role "
                    "(update-alternatives, s251-D11); a number about no role orders "
                    "nothing." % (name, p))
            else:
                prio.setdefault(role, {}).setdefault(p, []).append(name)

        # 7 intent-equals-answers
        if "intent" in d and "answers" in d:
            iw, iok = _words(d["intent"])
            aw, aok = _words(d["answers"])
            if iok and aok and sorted(iw) != sorted(aw):
                fails.append(
                    "%s: FAIL [intent-equals-answers] — `intent` %r and `answers` %r "
                    "DISAGREE. `answers` is the general field and `intent` is kept, not "
                    "renamed (#253); two homes for one fact must at least agree — change "
                    "one, or drop `intent` by ruling." % (name, d["intent"], d["answers"]))

        # 8 span-ordered
        if "span" in d:
            cols = (d["span"] or {}).get("cols") if isinstance(d["span"], dict) else None
            if not isinstance(cols, dict):
                fails.append("%s: FAIL [span-ordered] — `span` must be {cols:{min,max}} "
                             "(s251-D10, 12-col canon), got %r" % (name, d["span"]))
            else:
                lo, hi = cols.get("min"), cols.get("max")
                if not isinstance(lo, int) or not isinstance(hi, int):
                    fails.append("%s: FAIL [span-ordered] — `span.cols.min`/`max` must be "
                                 "integers, got %r/%r" % (name, lo, hi))
                elif lo > hi:
                    fails.append("%s: FAIL [span-ordered] — `span.cols.min` %d > `max` %d. "
                                 "The 1..12 bounds are the schema's; draft-07 cannot "
                                 "compare two siblings, so the ORDER is checked here."
                                 % (name, lo, hi))

        # 9 shape-known (s254-D2 item 1 — the vocabulary is CLOSED as of #254)
        if "shape" in d:
            sv = d["shape"]
            if not isinstance(sv, str):
                fails.append("%s: FAIL [shape-known] — `shape` must be a single value "
                             "(string), got %r" % (name, sv))
            else:
                stats["addresses"] += 1
                stats["shape_values"].setdefault(sv, []).append(name)
                if sv not in shapes:
                    fails.append(
                        "%s: FAIL [shape-known] — UNKNOWN SHAPE %r — not a key of `shapes` "
                        "in knowledge/shapes.json. Legal set: %s. s254-D2 item 1 CLOSED "
                        "this vocabulary on page B's grammar `<x-dimension> × <mark>`: a "
                        "new value is PROPOSED on a review page and added by Dave's "
                        "ruling, NEVER silently by a lane."
                        % (name, sv, ", ".join(legal_shapes)))

        # 10 when-fields-known (s254-D2 item 2 — the further ruling s251-D5 deferred)
        if "when" in d:
            wv = d["when"]
            if not isinstance(wv, str):
                fails.append("%s: FAIL [when-fields-known] — `when` must be a predicate "
                             "string (s251-D5), got %r" % (name, wv))
            else:
                stats["when_fields"].append((name, wv))
                gate = wv.split("—")[0]
                claims = when_field_claims(wv)
                stats["when_prose_clauses"] += (
                    len([c for c in re.split(r"\bAND\b|\bOR\b", gate) if c.strip()])
                    - len(claims))
                for fld, clause in claims:
                    stats["when_field_counts"].setdefault(fld, []).append(name)
                    if fld not in whenf:
                        fails.append(
                            "%s: FAIL [when-fields-known] — UNKNOWN `when` FIELD %r in "
                            "clause %r — not a key of `fields` in "
                            "knowledge/when-fields.json. Legal set: %s. s251-D5 ruled "
                            "`when` a PREDICATE and deferred the field list; s254-D2 item "
                            "2 closed it. A lane does not add a name to make its own "
                            "predicate parse." % (name, fld, clause[:80],
                                                  ", ".join(legal_when)))

    # 5 priority-unique (after the sweep — a tie needs both members named)
    for r in sorted(prio):
        for p in sorted(prio[r]):
            who = prio[r][p]
            if len(who) > 1:
                fails.append(
                    "%s: FAIL [priority-unique] — priority %d is claimed by %d providers "
                    "of role %r: %s. Priority is the in-role ORDER; a tie makes the "
                    "default provider unreadable." % (who[0], p, len(who), r,
                                                      ", ".join(who)))

    return fails, stats


# ------------------------------------------------------------------- derivations
def _span_overlaps(a, b):
    try:
        return not (a["cols"]["max"] < b["cols"]["min"] or b["cols"]["max"] < a["cols"]["min"])
    except Exception:
        return None


def derive(docs, roles):
    """DERIVE the reciprocals. Returns a dict of printable lines. WRITES NOTHING.

    s251-D6: author one direction, the validator derives the other. ISO 25964: within a
    set of equivalent terms one is PREFERRED (here: the highest `priority`), the rest are
    non-preferred entry terms pointing at it.
    """
    out = {"instead-of": [], "not-with": [], "with": [], "preferred": []}

    # instead-of: co-providers of one role, graded on the other two FFF faces
    by_role = {}
    for name, d in docs.items():
        r = d.get("provides")
        if isinstance(r, str) and r in roles:
            by_role.setdefault(r, []).append(name)
    for r in sorted(by_role):
        members = sorted(by_role[r],
                         key=lambda n: (-(docs[n].get("priority") or 0), n))
        if len(members) < 2:
            continue
        pref = members[0]
        out["preferred"].append(
            "role %-16s PREFERRED TERM %s (priority %s) — %d co-provider(s)"
            % (r, pref, docs[pref].get("priority"), len(members) - 1))
        for m in members[1:]:
            a, b = docs[m], docs[pref]
            same_shape = ("shape" in a and "shape" in b and a["shape"] == b["shape"])
            ov = (_span_overlaps(a["span"], b["span"])
                  if isinstance(a.get("span"), dict) and isinstance(b.get("span"), dict)
                  else None)
            faces = int(bool(same_shape)) + int(ov is True)
            grade = "equivalent" if faces == 2 else ("near" if faces == 1 else "distant")
            out["instead-of"].append(
                "%-28s instead-of %-28s [%s] role=%s shape=%s span=%s"
                % (m, pref, grade, r,
                   "same" if same_shape else "differs",
                   {True: "overlaps", False: "disjoint", None: "unknown"}[ov]))

    # not-with reciprocals — exclusion is symmetric
    declared = {(n, e["slug"]) for n, d in docs.items()
                for e in (d.get("not-with") or []) if isinstance(e, dict)
                and isinstance(e.get("slug"), str)}
    for src, dst in sorted(declared):
        if dst not in docs:
            out["not-with"].append("%-28s not-with %-28s -> reciprocal NOT DERIVABLE "
                                   "(target is a ROLE, not a meta)" % (dst, src))
        elif (dst, src) in declared:
            out["not-with"].append("%-28s not-with %-28s -> already-authored" % (dst, src))
        else:
            out["not-with"].append("%-28s not-with %-28s -> DERIVED (symmetric)" % (dst, src))

    # with reciprocals — WEAK, flagged; a complement is not symmetric in general
    dwith = {(n, e["slug"], e.get("rel", "suggests")) for n, d in docs.items()
             for e in (d.get("with") or []) if isinstance(e, dict)
             and isinstance(e.get("slug"), str)}
    for src, dst, rel in sorted(dwith):
        if dst not in docs:
            out["with"].append("%-28s with %-28s -> reciprocal NOT DERIVABLE "
                               "(target is a ROLE, not a meta)" % (dst, src))
        else:
            out["with"].append("%-28s with %-28s -> DERIVED suggests (from %s; NOT "
                               "asserted — a complement is one-way until Dave says "
                               "otherwise)" % (dst, src, rel))
    return out


def cross_check(docs, roles):
    """roles.json membership vs the metas' `provides`. REPORT, never fail (s252-D1)."""
    lines = []
    carriers = {n: d["provides"] for n, d in docs.items()
                if isinstance(d.get("provides"), str)}
    if not carriers:
        lines.append("ZERO metas carry `provides` — the cross-check has NOTHING to compare. "
                     "This is a REPORT OF ABSENCE, not agreement: read no green from it. "
                     "(s252-D1: roles.json membership is the source until the 25-meta pass "
                     "authors the metas, then the metas are canon and this list is the "
                     "cross-check.)")
        return lines
    for r in sorted(roles):
        listed = {p["slug"] for p in roles[r].get("providers", [])
                  if isinstance(p, dict) and isinstance(p.get("slug"), str)}
        authored = {n for n, v in carriers.items() if v == r}
        for m in sorted(authored - listed):
            lines.append("role %-16s meta %s declares it; roles.json does NOT list it "
                         "(report only)" % (r, m))
        for m in sorted(listed - authored):
            if m in docs and m in carriers:
                lines.append("role %-16s roles.json lists %s; that meta declares %r "
                             "(report only)" % (r, m, carriers[m]))
    if not lines:
        lines.append("roles.json membership and the metas' `provides` AGREE for every "
                     "meta that carries the field (%d)." % len(carriers))
    return lines


# --------------------------------------------------------------------------- main
def main():
    fails, stats = check()
    docs, _ = read_corpus()
    roles = load_roles()
    print("roles resolve — metas: %d · carrying an interchangeability term: %d · "
          "addresses resolved: %d" % (stats["metas"], stats["carrying"], stats["addresses"]))
    print("  field population: " + " · ".join("%s %d" % (t, stats["counts"][t]) for t in TERMS))

    shapes = load_shapes()
    whenf = load_when_fields()
    if stats["shape_values"]:
        print("  `shape` values in use (%d of the %d in knowledge/shapes.json — CLOSED "
              "store, s254-D2 item 1): " % (len(stats["shape_values"]), len(shapes))
              + " · ".join("%s (%d)" % (k, len(v))
                           for k, v in sorted(stats["shape_values"].items())))
        unused = sorted(set(shapes) - set(stats["shape_values"]))
        if unused:
            print("    store values with NO carrier (reported, not a fail): "
                  + " · ".join(unused))
    else:
        print("  `shape`: no values in use (the store has %d)" % len(shapes))
    if stats["when_field_counts"]:
        print("  `when` FIELD COUNTS (%d of the %d in knowledge/when-fields.json — "
              "SCRIPT OUTPUT, quote these on a review page rather than counting by eye; "
              "this is what closes V-B's M2):"
              % (len(stats["when_field_counts"]), len(whenf)))
        for f in sorted(stats["when_field_counts"],
                        key=lambda k: (-len(stats["when_field_counts"][k]), k)):
            who = stats["when_field_counts"][f]
            print("    %-14s %2d  %s" % (f, len(who), ", ".join(sorted(who))))
        nf = sorted(set(whenf) - set(stats["when_field_counts"]))
        if nf:
            print("    legal fields with NO clause (reported, not a fail): "
                  + " · ".join(nf))
        print("    gate clauses carrying NO operator (prose inside the gate — not parsed, "
              "not judged, V-B's M2 method): %d" % stats["when_prose_clauses"])
    if stats["when_fields"]:
        print("  `when` predicates as authored:")
        for n, w in stats["when_fields"]:
            print("    %-28s %s" % (n, w))
    else:
        print("  `when`: no predicates authored yet")

    d = derive(docs, roles)
    print("DERIVED (printed, NEVER written into a meta — s251-D6, ISO 25964):")
    for key in ("preferred", "instead-of", "not-with", "with"):
        if d[key]:
            for line in d[key]:
                print("    %-11s %s" % (key + ":", line))
    if not any(d.values()):
        print("    nothing to derive — no meta carries `provides`, `not-with` or `with` yet.")

    print("CROSS-CHECK roles.json <-> metas (REPORT ONLY, never a fail — s252-D1):")
    for line in cross_check(docs, roles):
        print("    " + line)

    if fails:
        print("\n".join(fails))
        print("RESULT: FAIL (%d)" % len(fails))
        return 1
    print("RESULT: PASS — every role/answers/shape/not-with/with address resolves, every "
          "`when` field name is legal, priorities are unique in-role, and intent agrees "
          "with answers. This proves no address DANGLES; it does not prove any assignment "
          "is RIGHT (Dave's eye, against each meta's own `purpose` prose), and it does not "
          "prove a `when` predicate is TRUE of its component — only that its field names "
          "are in the store.")
    return 0


# --------------------------------------------------------------------------- selftest
def selftest():
    """15 bites. Each must return the named verdict, or the check is decorative."""
    import shutil
    import tempfile
    ok = True

    def bite(name, expect_fail, build):
        nonlocal ok
        tmp = tempfile.mkdtemp()
        try:
            cdir = os.path.join(tmp, "components")
            os.makedirs(cdir)
            rp = os.path.join(tmp, "roles.json")
            ip = os.path.join(tmp, "chart-intents.json")
            sp = os.path.join(tmp, "shapes.json")
            wp = os.path.join(tmp, "when-fields.json")
            stores(rp, ip, sp, wp)
            build(cdir, rp, ip)
            try:
                fails, _ = check(cdir, rp, ip, sp, wp)
                got = bool(fails)
                detail = fails[0] if fails else "(green)"
            except SystemExit as e:
                got, detail = True, str(e)
            good = (got == expect_fail)
            ok = ok and good
            print("  %s %-38s -> %s | %s" % ("PASS" if good else "BITE-MISSED", name,
                                             "FAIL" if got else "green", detail[:110]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def stores(rp, ip, sp, wp):
        json.dump({"roles": {"chart-panel": {"providers": [{"slug": "chart-bar"}]},
                             "headline-metric": {"providers": []}}},
                  open(rp, "w", encoding="utf-8"))
        json.dump({"chart-intent": {w: {"definition": "x"} for w in
                                    ("comparison", "distribution", "change-over-time")}},
                  open(ip, "w", encoding="utf-8"))
        json.dump({"shapes": {s: {"definition": "x"} for s in
                              ("series", "categories × series")}},
                  open(sp, "w", encoding="utf-8"))
        json.dump({"fields": {f: {"definition": "x"} for f in
                              ("span.cols", "answers", "shape", "series")}},
                  open(wp, "w", encoding="utf-8"))

    def meta(cdir, name, **kw):
        d = {"name": name, "purpose": "p"}
        d.update({k.replace("_", "-"): v for k, v in kw.items()})
        json.dump(d, open(os.path.join(cdir, "%s.meta.json" % name), "w", encoding="utf-8"))

    print("selftest — _validate_roles_resolve.py")
    bite("a fully-tagged meta resolves", False,
         lambda c, r, i: meta(c, "chart-bar", provides="chart-panel", answers="comparison",
                              shape="series", span={"cols": {"min": 6, "max": 12}},
                              priority=60, when="span.cols >= 6"))
    # ^ the `when` here was `span >= 6` until #254. Check 10 (s254-D2 item 2) refused it:
    # `span` is not a legal field name, `span.cols` is. The FIXTURE was corrected, not the
    # check — a stale bite is exactly what a new check is supposed to catch.
    bite("unknown role refuses", True,
         lambda c, r, i: meta(c, "Bad", provides="chart-pane"))
    bite("unknown answer refuses", True,
         lambda c, r, i: meta(c, "Bad2", answers=["comparison", "count-vs-threshold"]))
    bite("not-with slug resolving to nothing refuses", True,
         lambda c, r, i: meta(c, "Bad3", not_with=[{"slug": "ghost-card"}]))
    bite("duplicate priority inside one role refuses", True,
         lambda c, r, i: (meta(c, "A", provides="chart-panel", priority=60),
                          meta(c, "B", provides="chart-panel", priority=60)))
    bite("same priority in DIFFERENT roles is legal", False,
         lambda c, r, i: (meta(c, "A", provides="chart-panel", priority=60),
                          meta(c, "B", provides="headline-metric", priority=60)))
    bite("priority with no provides refuses", True,
         lambda c, r, i: meta(c, "Bad6", priority=60))
    bite("intent != answers refuses", True,
         lambda c, r, i: meta(c, "Bad4", intent="comparison", answers="distribution"))
    bite("span min > max refuses", True,
         lambda c, r, i: meta(c, "Bad5", span={"cols": {"min": 9, "max": 4}}))
    bite("absent roles store fails LOUD", True,
         lambda c, r, i: (os.remove(r), meta(c, "Orphan", provides="chart-panel")))
    bite("unknown shape refuses", True,
         lambda c, r, i: meta(c, "Bad7", shape="bins × frequency"))
    bite("a shape IN the store resolves", False,
         lambda c, r, i: meta(c, "Ok7", shape="categories × series"))
    bite("unknown `when` field refuses", True,
         lambda c, r, i: meta(c, "Bad8", when="prominence >= 2 — beats nothing"))
    bite("prose in the gate is NOT a field claim", False,
         lambda c, r, i: meta(c, "Ok8", when="answers = comparison AND parts sum to a "
                                             "whole — beats nothing"))
    bite("a field named only AFTER the em-dash is not parsed", False,
         lambda c, r, i: meta(c, "Ok9", when="series != none — yields when prominence "
                                             "= low, which is prose"))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# -------------------------------------------------------------------- mutation harness
# ⛔ #244: a mutation the check never READS is not a bite. PROBED FIRST, on the live corpus:
# today ZERO metas carry any of the eight terms, so a mutation that only edits `shape` or
# adds a `when` would change NOTHING the checks read and would "pass" as a false negative.
# Every arm below therefore mutates a field a NAMED check reads, on an IN-MEMORY COPY of a
# LIVE meta plus the LIVE stores. No file on disk is written, moved or restored, because
# none is ever touched. Each arm declares the verdict it EXPECTS (s182-D1: the claim
# carries its probe) — including a GREEN arm, so the harness is not a one-way ratchet.
MUTATIONS = {
    "unknown-role": ("chart-bar gains provides='chart-pane' (a typo for a real role)", "RED"),
    "known-role": ("chart-bar gains provides='chart-panel' (the true role)", "GREEN"),
    "unknown-answer": ("chart-bar gains answers='count-vs-threshold' (unruled word)", "RED"),
    "answer-disagrees": ("chart-bar gains answers='distribution' against intent='comparison'", "RED"),
    "dup-priority": ("chart-bar + chart-line both provide chart-panel at priority 60", "RED"),
    "span-inverted": ("chart-bar gains span cols min 9 > max 4", "RED"),
    "notwith-ghost": ("chart-bar gains not-with slug 'ghost-card'", "RED"),
    "derive-demo": ("chart-bar + chart-line tagged legally, with a not-with edge — the arm "
                    "that DRIVES derive(): the reciprocals must actually PRINT", "GREEN"),
    "unknown-shape": ("chart-bar's shape becomes 'categories-by-series' — the PRE-#254 "
                      "page-A spelling, now re-cut out of the store (s254-D2 item 1)",
                      "RED"),
    "known-shape": ("chart-bar's shape becomes 'parts-of-whole' — a value that IS in the "
                    "store, wrong for a bar chart but LEGAL: the check reads the store, "
                    "not the meaning", "GREEN"),
    "unknown-when-field": ("chart-bar's `when` gate gains 'prominence >= 2' — a field name "
                           "no store admits (s254-D2 item 2)", "RED"),
    "when-prose-not-parsed": ("chart-bar's `when` gains a prose clause with NO operator "
                              "('the reader already knows the categories') — the arm that "
                              "proves prose is not read as a field claim", "GREEN"),
}


def mutate(name):
    import shutil
    import tempfile
    what, want = MUTATIONS[name]
    docs, _ = read_corpus()
    base_fails, _ = check()
    tmp = tempfile.mkdtemp()
    try:
        cdir = os.path.join(tmp, "components")
        shutil.copytree(COMP, cdir)          # a COPY; the live tree is never touched
        bar = os.path.join(cdir, "chart-bar.meta.json")
        line = os.path.join(cdir, "chart-line.meta.json")
        d = copy.deepcopy(docs["chart-bar"])
        if name == "unknown-role":
            d["provides"] = "chart-pane"
        elif name == "known-role":
            d["provides"] = "chart-panel"
        elif name == "unknown-answer":
            d["answers"] = "count-vs-threshold"
        elif name == "answer-disagrees":
            d["answers"] = "distribution"
        elif name == "dup-priority":
            d["provides"], d["priority"] = "chart-panel", 60
            e = copy.deepcopy(docs["chart-line"])
            e["provides"], e["priority"] = "chart-panel", 60
            json.dump(e, open(line, "w", encoding="utf-8"))
        elif name == "span-inverted":
            d["span"] = {"cols": {"min": 9, "max": 4}}
        elif name == "notwith-ghost":
            d["not-with"] = [{"slug": "ghost-card"}]
        elif name == "derive-demo":
            # The fixture's values were `shape: series` / priorities 60 and 50 until #254,
            # written when ZERO metas carried a term. Check 9 (shape-known) refused the
            # invented shape and priority 60 now collides with a live provider — so the
            # FIXTURE moved to the store's own values and the metas' own priorities. The
            # arm still drives derive(); nothing about the check was relaxed.
            d["provides"], d["priority"] = "chart-panel", 92
            d["shape"] = "categories × series"
            d["span"] = {"cols": {"min": 6, "max": 12}}
            d["not-with"] = [{"slug": "chart-line", "when": "span.cols < 6"}]
            e = copy.deepcopy(docs["chart-line"])
            e["provides"], e["priority"] = "chart-panel", 88
            e["shape"] = "categories × series"
            e["span"] = {"cols": {"min": 6, "max": 12}}
            e["with"] = [{"slug": "chart-bar", "rel": "recommends"}]
            json.dump(e, open(line, "w", encoding="utf-8"))
        elif name == "unknown-shape":
            d["shape"] = "categories-by-series"
        elif name == "known-shape":
            d["shape"] = "parts-of-whole"
        elif name == "unknown-when-field":
            d["when"] = ("answers = comparison AND prominence >= 2 — beats chart-line "
                         "when the x-dimension is categorical")
        elif name == "when-prose-not-parsed":
            d["when"] = ("answers = comparison AND the reader already knows the "
                         "categories — beats chart-line when the x-dimension is "
                         "categorical")
        json.dump(d, open(bar, "w", encoding="utf-8"))
        fails, stats = check(cdir, ROLES, INTENTS, SHAPES, WHENF)
        mdocs, _ = read_corpus(cdir)
        derived = derive(mdocs, load_roles())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # The verdict is BASELINE-RELATIVE (#254): does THIS mutation make the check say
    # something it was not already saying? It was `bool(fails)` until #254, which silently
    # assumed the live corpus is green. It is not: runway-bar carries a RED-BY-DESIGN
    # intent/answers disagreement (s254-D2 item 4 is DATED, not built), and that one
    # standing fail made all four GREEN arms unprovable — a harness that cannot be driven
    # is [[instrument-without-a-consumer]]. The CHECK is untouched and no fail is hidden:
    # the baseline is printed, and every arm still proves the check READS its field.
    new_fails = [f for f in fails if f not in base_fails]
    got = "RED" if new_fails else "GREEN"
    print("MUTATION %s — %s" % (name, what))
    print("  baseline : live corpus %s (%d fail(s)) — probed BEFORE the claim (#244)"
          % ("RED" if base_fails else "GREEN", len(base_fails)))
    for x in base_fails[:2]:
        print("  = " + x[:200])
    print("  mutated  : %d fail(s), %d NEW · metas carrying a term now %d (baseline 0 "
          "would mean the check reads NOTHING)"
          % (len(fails), len(new_fails), stats["carrying"]))
    for x in new_fails[:4]:
        print("  X " + x[:200])
    nd = sum(len(v) for v in derived.values())
    print("  derived  : %d reciprocal/preferred line(s) — printed, never written" % nd)
    for key in ("preferred", "instead-of", "not-with", "with"):
        for ln in derived[key]:
            print("    %-11s %s" % (key + ":", ln))
    print("  expected %s · got %s — %s" % (want, got, "OK" if got == want else
                                           "MUTATION NOT PROVEN"))
    return 0 if got == want else 1


if __name__ == "__main__":
    if "--mutate" in sys.argv:
        i = sys.argv.index("--mutate")
        nm = sys.argv[i + 1] if len(sys.argv) > i + 1 else ""
        if nm not in MUTATIONS:
            print("--mutate takes one of: " + " · ".join(sorted(MUTATIONS)))
            sys.exit(2)
        sys.exit(mutate(nm))
    sys.exit(selftest() if "--selftest" in sys.argv else main())
