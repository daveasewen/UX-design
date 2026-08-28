#!/usr/bin/env python3
"""_search_core.py — the retrieval spine: ONE engine, N corpus doors (O2′, ruled 2026-07-28 #25).

Ruled direction (Dave, `notes/_MEMENTO-DECISIONS.md` § Memento-before-Apollo + § ★ #25):
split `_consult.py` into a CORE (index + query + fail-loud contract, TWO-STAGE:
stage 1 returns refs — ids + one-liners; stage 2 fetches the record body verbatim as a
separate step) plus corpus ADAPTERS. The doors:

  knowledge/_consult.py          — the DS-decisions door (exists since ds-009; now thin)
  knowledge/_memento_search.py   — the Memento door (GM/LS sections · archives · briefs ·
                                   ledgers · runbooks · lanes), index built by
                                   `_build_memento_index.py` — which lives in `knowledge/`
                                   in this repo and in `memento-package/machinery/` in a
                                   shipped pack. This file runs, byte-identical, in BOTH:
                                   name the builder, never a tree-specific path to it.

One retrieval spine, three customers — the third is the KG forcing function (floated by
Dave 2026-07-27, scoped in by him mid-flight #25): the consult-receipt line FORMAT lives
HERE, one copy, and `_capture_gate.py::consult_receipt_probe` IMPORTS it (the mover≠gate
lesson — logic is imported, never re-implemented).

Fail-loud contract (ds-016 class):
  - fetch of an unknown id REFUSES, with near-misses listed — never a silent empty result;
  - an empty record set REFUSES at load — a door with nothing to search is broken, not quiet;
  - doors must never enumerate-and-skip malformed corpus structure — unknown forms refuse
    in the door's builder, not here.

Honest denominators: group headers say `(3)` when 3 is everything, and
`(5 of 12 shown — --all for more)` only when a cap actually bit (closes the §C·4
"5/5 shown" enact-queue wart — the old header quoted the CAP as the denominator).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, re, sys

STOPWORDS = {
    "the", "and", "for", "with", "on", "of", "a", "an", "in", "to", "is", "are",
    "it", "its", "be", "as", "at", "by", "or", "this", "that", "we", "our",
}


def tokenize(s):
    return [t for t in re.split(r"[^a-z0-9]+", s.lower()) if len(t) >= 3 and t not in STOPWORDS]


def expand_query(raw_query, lexicon):
    """Original query tokens, plus lexicon-expanded tokens. Returns (original_set, expanded_only_set)."""
    original = set(tokenize(raw_query))
    expanded = set()
    lc = raw_query.lower()
    for key, val in (lexicon or {}).get("synonyms", {}).items():
        if key in lc:
            expanded |= set(tokenize(val))
    expanded -= original
    return original, expanded


def stem_candidates(token):
    """A few cheap candidate substrings for a query token, so 'fonts' still finds 'font-size'
    and 'portability' still finds 'portable'. Not real stemming — substring search is."""
    cands = {token}
    if token.endswith("ing") and len(token) > 5:
        cands.add(token[:-3])
    if token.endswith("es") and len(token) > 4:
        cands.add(token[:-2])
    if token.endswith("s") and len(token) > 3:
        cands.add(token[:-1])
    if len(token) > 6:
        cands.add(token[:6])
    return {c for c in cands if len(c) >= 3}


def record_blob(r):
    return " ".join(str(r.get(k, "")) for k in ("id", "kind", "file", "head", "text", "status")).lower()


def score_record(record, original_tokens, expanded_tokens):
    blob = record_blob(record)
    matched_original = 0
    for t in original_tokens:
        if any(c in blob for c in stem_candidates(t)):
            matched_original += 1
    matched_expanded = 0
    for t in expanded_tokens:
        if any(c in blob for c in stem_candidates(t)):
            matched_expanded += 1
    return matched_original * 2 + matched_expanded


def search(records, query, lexicon, bucket_fn, caps, all_results=False, decorate=None):
    """Stage 1. Generic ranked retrieval: bucket_fn(record) → bucket id or None (skip);
    decorate(entry) may add door-specific columns (e.g. the DS enforcement line).
    Returns (buckets, totals, original, expanded) — totals are PRE-CAP counts, so doors
    can print honest denominators."""
    original, expanded = expand_query(query, lexicon)
    buckets, totals = {}, {}
    for r in records:
        b = bucket_fn(r)
        if b is None:
            continue
        s = score_record(r, original, expanded)
        if s <= 0:
            continue
        entry = dict(r)
        entry["_score"] = s
        if decorate:
            decorate(entry)
        buckets.setdefault(b, []).append(entry)
    for b in list(buckets):
        buckets[b].sort(key=lambda e: (-e["_score"], len(e.get("text", "")), e["id"]))
        totals[b] = len(buckets[b])
        if not all_results and caps and b in caps:
            buckets[b] = buckets[b][: caps[b]]
    return buckets, totals, original, expanded


def fetch(records, record_id):
    """Stage 2. Exact-id lookup → (record, None) or (None, refusal_message).
    REFUSES on a miss — a wrong id must never read as an empty-but-fine result."""
    by_id = {}
    for r in records:
        by_id.setdefault(r["id"], r)
    if record_id in by_id:
        return by_id[record_id], None
    q = record_id.lower()
    near = [i for i in sorted(by_id) if q in i.lower() or i.lower() in q][:5]
    if not near:
        qt = set(tokenize(record_id))
        near = [i for i in sorted(by_id) if qt & set(tokenize(i))][:5]
    if not near:  # short ids (`B-9`) tokenize to nothing — fall back to the leading run
        m = re.match(r"[a-z0-9]+", q)
        if m:
            near = [i for i in sorted(by_id) if i.lower().startswith(m.group(0))][:5]
    return None, ("fetch: unknown id `%s` — REFUSING (fail-loud; ds-016 class). %s"
                  % (record_id,
                     "Near misses: " + " · ".join(near) if near else "No near misses."))


def group_header(label, shown, total, all_results=False, cap_hint="--all for more"):
    """Honest denominator: quote the TOTAL matched, and only when a cap actually bit."""
    if all_results or shown >= total:
        return f"{label} ({shown}):"
    return f"{label} ({shown} of {total} shown — {cap_hint}):"


# ------------------------------------------------------- naming the builder, in EITHER tree
# ⛔ #221 (from #220's L4 audit, finding F3). The missing-index refusal below used to TYPE
# `python3 knowledge/_build_all.py`. That path is true in this repo and FALSE in every shipped
# pack: `_build_all.py` is not on the ship list, so a designer's very first retrieval attempt —
# the one `.github/copilot-instructions.md` operating rule 2 sends them to — refused with a
# pointer to a file they do not have, while the builder that DOES ship
# (`memento-package/machinery/_build_memento_index.py`, driven clean from a virgin unzip at
# #220-L4) sat two directories away. Retrieval is half of what Memento is, and it was one
# filename from working.
#
# A typed path cannot be right in two trees. The fix is RESOLUTION, not a second typed string
# [[gate-dont-patch]]: derive the builder's NAME from the index's own name, then look for it on
# disk beside the index (both trees keep the builder next to what it writes) and one level up.
# Nothing found ⇒ say so; a measuring tool must not guess, and naming a script the reader does
# not have is worse than admitting the builder cannot be located.
BUILDER_FALLBACKS = ("_build_all.py",)


def builder_names_for(index_path):
    """The builder filename(s) this index's own name implies, most specific first.

    `_memento-index.json` → `_build_memento_index.py`; `_consult-index.json` →
    `_build_consult_index.py`. Derived, never a lookup table that can rot behind a new door.
    """
    stem = re.sub(r"\.json$", "", os.path.basename(index_path)).lstrip("_")
    names = []
    if stem.endswith("-index"):
        names.append("_build_%s_index.py" % stem[: -len("-index")].replace("-", "_"))
    return tuple(names) + BUILDER_FALLBACKS


def index_builder_command(index_path):
    """`python3 <path to the builder that writes this index>`, resolved on disk — or None.

    None is a real answer and the caller says it out loud, rather than printing a path that
    exists in somebody else's tree.
    """
    d = os.path.dirname(os.path.abspath(index_path))
    for base in (d, os.path.dirname(d)):
        for name in builder_names_for(index_path):
            cand = os.path.join(base, name)
            if os.path.isfile(cand):
                rel = os.path.relpath(cand, os.getcwd())
                return "python3 %s" % (cand if rel.startswith("..") else rel)
    return None


def load_records_or_refuse(index_path, what):
    """Load a door's index and REFUSE (SystemExit) if missing or empty — a door with
    nothing behind it is a broken door, not a quiet one."""
    if not os.path.exists(index_path):
        cmd = index_builder_command(index_path)
        how = ("run the build (%s)" % cmd) if cmd else (
            "and the builder that writes it is not beside it — this door cannot name what "
            "would build it, and will not invent a path")
        raise SystemExit(f"{what}: index missing at {index_path} — {how}; "
                         f"REFUSING to search nothing.")
    with open(index_path, encoding="utf-8") as f:
        data = json.load(f)
    records = data.get("records", [])
    if not records:
        raise SystemExit(f"{what}: index at {index_path} holds ZERO records — corpus glob "
                         f"broken? REFUSING (fail-loud, never enumerate-and-skip).")
    return data


# ---------------------------------------------------------------- consult receipts
# The KG forcing-function line format (Dave: floated 2026-07-27, scoped into O2′ #25).
# ONE copy — _capture_gate.py::consult_receipt_probe IMPORTS these. The stratum line:
#   > **consult-receipts #25:** "two lanes routing" → ledger:two-lanes · lane:lane-1-memento ; "amber fills" → R-D3
# or the honest negative:
#   > **consult-receipts #25:** none — pure enactment window, no design decisions taken
#
# RUNNING COUNT — ruled Dave 2026-08-02 (dream pass 4, P4 "ACCEPTED with a reframe"), inscribed #128.
# The stratum line CARRIES its own running count, "Nth of M", written after the session number:
#   > **consult-receipts #25 (18th of 40):** "two lanes routing" → ledger:two-lanes
#   > **consult-receipts #25 (18th of 40):** none — pure enactment window, no design decisions taken
# N = sessions whose receipts line is non-`none`; M = sessions carrying a receipts line at all.
# FORM ONLY — history is NOT re-stamped, and the count is NOT gated (the rate is a question about
# the TOOL, not about discipline: ~50% `none` across 40 sessions, flat, several of them legitimate).
# The optional `(Nth of M)` group is the 2026-08-02 running count (inscribed #128). It is
# ACCEPTED, never REQUIRED — lines written before the form, and lines written without it,
# parse exactly as they did. No new failure mode is introduced by this group.
RECEIPT_LINE_RE = re.compile(
    r"^>\s*\*\*consult-receipts\s+#(\d+)(?:\s*\((?:\d+)(?:st|nd|rd|th)\s+of\s+(?:\d+)\))?:\*\*\s*(.+?)\s*$")
_RECEIPT_NONE_RE = re.compile(r"^none\s*[—–-]\s*\S.+$")
_RECEIPT_SEG_RE = re.compile(r'^"([^"]+)"\s*→\s*(\S.*)$')


def validate_receipt_payload(payload):
    """FORM-check the payload after the marker. Returns a list of error strings.
    FORM only — whether the queries were actually run is testimony, not observation
    (the pre-flight-stamp / section-usage precedent, stated not hidden)."""
    errors = []
    payload = payload.strip()
    if _RECEIPT_NONE_RE.match(payload):
        return errors
    if payload == "none" or payload.startswith("none"):
        errors.append('consult-receipts: bare `none` — the honest negative needs its why: '
                      '`none — <reason>`')
        return errors
    segs = [s.strip() for s in payload.split(";") if s.strip()]
    if not segs:
        errors.append("consult-receipts: empty payload — receipts or `none — <why>`")
        return errors
    for seg in segs:
        m = _RECEIPT_SEG_RE.match(seg)
        if not m:
            errors.append(f'consult-receipts: segment does not parse as `"query" → ids`: '
                          f"{seg[:60]}")
            continue
        ids = [i.strip() for i in m.group(2).split("·") if i.strip()]
        if not ids:
            errors.append(f'consult-receipts: query "{m.group(1)[:40]}" carries no record ids '
                          f"— a receipt with no retrieved ids is a claim, not a receipt")
    return errors


# ------------------------------------------------------------------ selftest
def selftest():
    """Every check proves the engine can FAIL — green-by-construction is not a test."""
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    recs = [
        {"id": "A-1", "kind": "x", "file": "f.md", "head": "font-size rules", "text": "the font-size ramp"},
        {"id": "A-2", "kind": "x", "file": "f.md", "head": "colour", "text": "amber on white"},
        {"id": "B-1", "kind": "y", "file": "g.md", "head": "lanes", "text": "lane routing check"},
    ]
    # matching + stem: plural query finds singular text
    b, t, _, _ = search(recs, "fonts", None, lambda r: r["kind"], {"x": 5, "y": 5})
    bite("stem: 'fonts' finds the font-size record", [e["id"] for e in b.get("x", [])] == ["A-1"])
    # scoring can MISS — an unrelated query returns nothing
    b, t, _, _ = search(recs, "quaternion", None, lambda r: r["kind"], {"x": 5, "y": 5})
    bite("miss: unrelated query returns zero buckets", not b)
    # caps + honest totals
    many = [{"id": f"C-{i}", "kind": "x", "file": "f", "head": "amber", "text": "amber"} for i in range(7)]
    b, t, _, _ = search(many, "amber", None, lambda r: r["kind"], {"x": 3})
    bite("cap bites at 3, total honest at 7", len(b["x"]) == 3 and t["x"] == 7)
    bite("header quotes total when capped", group_header("g", 3, 7) == "g (3 of 7 shown — --all for more):")
    bite("header quotes plain count when complete", group_header("g", 3, 3) == "g (3):")
    # fetch: hit, and REFUSAL on miss with near-miss listed
    r, err = fetch(recs, "B-1")
    bite("fetch hit returns the record", r is not None and r["id"] == "B-1" and err is None)
    r, err = fetch(recs, "B-9")
    bite("fetch miss REFUSES", r is None and "REFUSING" in err)
    bite("fetch miss lists a near-miss", "B-1" in err)
    # receipts: good forms pass, bad forms fail
    bite("receipt: query→ids form passes",
         validate_receipt_payload('"two lanes" → ledger:two-lanes · lane:lane-1-memento') == [])
    bite("receipt: honest negative passes",
         validate_receipt_payload("none — pure enactment window") == [])
    bite("receipt: bare none REFUSED", validate_receipt_payload("none") != [])
    bite("receipt: missing arrow REFUSED", validate_receipt_payload('"query" ledger:x') != [])
    bite("receipt: empty ids REFUSED", validate_receipt_payload('"query" → ') != [])
    # empty-index refusal
    try:
        load_records_or_refuse(os.path.join("/nonexistent", "_no-index.json"), "selftest")
        bite("empty/missing index REFUSES", False)
    except SystemExit as e:
        bite("empty/missing index REFUSES", "REFUSING" in str(e))

    # ---- #221/F3: the refusal's SIGNPOST, driven in BOTH directions -------------------------
    # A green over "it refused" was exactly what let the wrong builder path survive into a
    # shipped pack. These bites grade WHAT the refusal says, on a real tree built here.
    bite("builder name is DERIVED from the index name (memento door)",
         builder_names_for("/x/_memento-index.json")[0] == "_build_memento_index.py")
    bite("builder name is DERIVED from the index name (consult door)",
         builder_names_for("/x/_consult-index.json")[0] == "_build_consult_index.py")
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _d:
        _idx = os.path.join(_d, "_memento-index.json")
        # direction 1 — the builder IS there: the refusal must name THAT file, and it must
        # exist on this box.
        _bld = os.path.join(_d, "_build_memento_index.py")
        open(_bld, "w").write("# selftest stub\n")
        try:
            load_records_or_refuse(_idx, "selftest")
            bite("missing index names the builder BESIDE it", False)
        except SystemExit as e:
            _m = re.search(r"python3 ([^\s)]+)", str(e))   # stop at the closing paren
            bite("missing index names the builder BESIDE it",
                 bool(_m) and os.path.isfile(os.path.join(os.getcwd(), _m.group(1))
                                             if not os.path.isabs(_m.group(1)) else _m.group(1)))
            bite("the named builder is the DERIVED one, not a fallback",
                 "_build_memento_index.py" in str(e) and "_build_all.py" not in str(e))
        os.remove(_bld)
        # direction 2 — no builder anywhere: REFUSE to invent one. This is the arm that would
        # have caught F3: the old code printed `knowledge/_build_all.py` unconditionally.
        try:
            load_records_or_refuse(_idx, "selftest")
            bite("no builder on disk ⇒ names NO command", False)
        except SystemExit as e:
            bite("no builder on disk ⇒ names NO command",
                 "python3 " not in str(e) and "will not invent" in str(e))
            bite("no builder on disk ⇒ still REFUSES", "REFUSING" in str(e))

    if fails:
        print(f"selftest FAILED — {len(fails)} bite(s): {fails}")
        return 1
    print("selftest OK — engine, fetch refusal, honest denominators and receipt form all bite.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(__doc__)
    sys.exit(0)
