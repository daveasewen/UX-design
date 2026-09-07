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
  * `shape` has NO STORE — its vocabulary is NOT RULED (s251-D3…D8). This script COUNTS
    and LISTS the distinct values so a review page can show them; it cannot check them.
    Same for the field list inside a `when` predicate (s251-D5 explicitly defers it).
  * Presence is not this check's business: a meta carrying none of the eight is skipped.
    No gate, no ratchet, no glob width is decided here.

Usage:  python3 knowledge/_validate_roles_resolve.py              # check mode
        python3 knowledge/_validate_roles_resolve.py --selftest   # 8 bites
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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROLES = os.path.join(HERE, "roles.json")
INTENTS = os.path.join(HERE, "chart-intents.json")
COMP = os.path.join(HERE, "components")

TERMS = ("provides", "answers", "shape", "span", "priority", "when", "with", "not-with")


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


def check(comp_dir=COMP, roles_path=ROLES, intents_path=INTENTS):
    """Returns (fails, stats). Every offending value is NAMED with its file."""
    roles = load_roles(roles_path)
    vocab = load_answers(intents_path)
    docs, fails = read_corpus(comp_dir)
    legal_roles = sorted(roles)
    legal_answers = sorted(vocab)
    known_slugs = set(docs) | set(roles)

    stats = {"metas": len(docs), "carrying": 0, "addresses": 0,
             "shape_values": {}, "when_fields": [], "by_role": {},
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

        # free axes — collected, never judged (their vocabularies are NOT ruled)
        if isinstance(d.get("shape"), str):
            stats["shape_values"].setdefault(d["shape"], []).append(name)
        if isinstance(d.get("when"), str):
            stats["when_fields"].append((name, d["when"]))

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

    if stats["shape_values"]:
        print("  `shape` values in use (vocabulary NOT RULED — listed, not checked): "
              + " · ".join("%s (%d)" % (k, len(v)) for k, v in sorted(stats["shape_values"].items())))
    else:
        print("  `shape`: no values in use (vocabulary NOT RULED — nothing to list)")
    if stats["when_fields"]:
        print("  `when` predicates (field list NOT RULED — collected for the review page):")
        for n, w in stats["when_fields"]:
            print("    %-28s %s" % (n, w))
    else:
        print("  `when`: no predicates authored yet (field list NOT RULED, s251-D5)")

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
    print("RESULT: PASS — every role/answers/not-with/with address resolves, priorities are "
          "unique in-role, and intent agrees with answers. This proves no address DANGLES; "
          "it does not prove any assignment is RIGHT (Dave's eye, against each meta's own "
          "`purpose` prose), and it checks NOTHING about `shape` or the `when` field list, "
          "whose vocabularies are not ruled.")
    return 0


# --------------------------------------------------------------------------- selftest
def selftest():
    """8 bites. Each must return the named verdict, or the check is decorative."""
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
            stores(rp, ip)
            build(cdir, rp, ip)
            try:
                fails, _ = check(cdir, rp, ip)
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

    def stores(rp, ip):
        json.dump({"roles": {"chart-panel": {"providers": [{"slug": "chart-bar"}]},
                             "headline-metric": {"providers": []}}},
                  open(rp, "w", encoding="utf-8"))
        json.dump({"chart-intent": {w: {"definition": "x"} for w in
                                    ("comparison", "distribution", "change-over-time")}},
                  open(ip, "w", encoding="utf-8"))

    def meta(cdir, name, **kw):
        d = {"name": name, "purpose": "p"}
        d.update({k.replace("_", "-"): v for k, v in kw.items()})
        json.dump(d, open(os.path.join(cdir, "%s.meta.json" % name), "w", encoding="utf-8"))

    print("selftest — _validate_roles_resolve.py")
    bite("a fully-tagged meta resolves", False,
         lambda c, r, i: meta(c, "chart-bar", provides="chart-panel", answers="comparison",
                              shape="series", span={"cols": {"min": 6, "max": 12}},
                              priority=60, when="span >= 6"))
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
            d["provides"], d["priority"] = "chart-panel", 60
            d["shape"] = "series"
            d["span"] = {"cols": {"min": 6, "max": 12}}
            d["not-with"] = [{"slug": "chart-line", "when": "span < 6"}]
            e = copy.deepcopy(docs["chart-line"])
            e["provides"], e["priority"] = "chart-panel", 50
            e["shape"] = "series"
            e["span"] = {"cols": {"min": 6, "max": 12}}
            e["with"] = [{"slug": "chart-bar", "rel": "recommends"}]
            json.dump(e, open(line, "w", encoding="utf-8"))
        json.dump(d, open(bar, "w", encoding="utf-8"))
        fails, stats = check(cdir, ROLES, INTENTS)
        mdocs, _ = read_corpus(cdir)
        derived = derive(mdocs, load_roles())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    got = "RED" if fails else "GREEN"
    print("MUTATION %s — %s" % (name, what))
    print("  baseline : live corpus %s (%d fail(s)) — probed BEFORE the claim (#244)"
          % ("RED" if base_fails else "GREEN", len(base_fails)))
    print("  mutated  : %d fail(s) · metas carrying a term now %d (baseline 0 would mean "
          "the check reads NOTHING)" % (len(fails), stats["carrying"]))
    for x in fails[:4]:
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
