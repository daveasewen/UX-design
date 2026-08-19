#!/usr/bin/env python3
"""_join_claim_tables.py — the generated PM-wave diff (W-44, `s204-D1` item 1, leg 2).

WHAT IT IS FOR: the conductor reads ONE generated diff, never two documents. A claim JSONL
(the build-PM's) and a challenge JSONL (the adversarial verifier's) are joined on `id`, and
the output carries ONLY what needs a human: disagreements, untested rows, fence touches, new
findings, and claims nobody challenged. CONFIRMED collapses to a count.

⛔ THE GOVERNING RULE — IT SURFACES, IT NEVER SUPPRESSES. `s204-D1`: "a row it hides is a
decision nobody made." Concretely, four things a naive join would swallow and this one does not:
  · a CONFIRMED row that touches a FENCE — collapsed by count, invisible; here it SURFACES.
  · a claim with NO challenge row — invisible to an inner join; here it surfaces as UNCHALLENGED,
    because "nobody tested this" is exactly the state the wave must see.
  · a challenge row with no claim counterpart — surfaces as NEW.
  · a row that will not parse — LOUD, NAMED, with a residual count (`a-crash-is-not-a-fail`).
The selftest has a SUPPRESSION ARM that plants each of these and proves it appears.

CLASSES EMITTED
  DISAGREEMENT   verdict CONTRADICTED
  UNTESTED       verdict UNTESTED
  NEW            challenge row whose id matches no claim
  FENCE          either side carries a `fence` string — surfaced at ANY verdict
  UNCHALLENGED   claim row that no challenge row answers
  (CONFIRMED, unfenced, matched → a count, and only a count)

LOUD INCONSISTENCIES (rc=1, never a silent reclassification)
  · verdict=NEW on a row whose id DOES match a claim — NEW means unmatched, by definition.
  · an unmatched challenge row NOT marked NEW — it is either a typo'd join key or a finding
    that lost its label; both are decisions nobody made.

USAGE
  python3 knowledge/_join_claim_tables.py <claims.jsonl> <challenges.jsonl> [--md <out.md>]
  python3 knowledge/_join_claim_tables.py --selftest

EXIT CODES: 0 = joined, nothing inconsistent (surfaced rows are NOT a failure — they are the
product). 1 = parse residual or a loud inconsistency. 2 = bad invocation.

CONSUMER at birth: the conductor's seat at the PM-wave seam, per `s204-D1`. Declared: NOT
wired into `_build_all.py` or CI until driven in >= 1 real wave.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _claimtable as CT

ORDER = ["DISAGREEMENT", "NEW", "FENCE", "UNTESTED", "UNCHALLENGED"]


def join(claims, challenges):
    """(surfaced, confirmed_count, inconsistencies). Pure — no I/O, so the selftest can drive it."""
    by_id = {c["id"]: c for c in claims}
    surfaced, inconsistent, confirmed = [], [], 0
    answered = set()

    for ch in challenges:
        cl = by_id.get(ch["id"])
        if cl is not None:
            answered.add(ch["id"])
        verdict = ch["verdict"]
        fence = ch.get("fence") or (cl.get("fence") if cl else "")

        if verdict == "NEW" and cl is not None:
            inconsistent.append("%s: verdict=NEW but a claim row with that id EXISTS "
                                "(%s:%d) — NEW means unmatched, by definition"
                                % (ch["id"], cl["_src"], cl["_lineno"]))
        if verdict != "NEW" and cl is None:
            inconsistent.append("%s: verdict=%s but NO claim row has that id — a typo'd join key "
                                "or a finding that lost its NEW label; either way a lost row"
                                % (ch["id"], verdict))

        if verdict == "CONTRADICTED":
            cls = "DISAGREEMENT"
        elif verdict == "UNTESTED":
            cls = "UNTESTED"
        elif verdict == "NEW" or cl is None:
            cls = "NEW"
        elif fence:
            cls = "FENCE"          # ⛔ a CONFIRMED row that touches a fence is NOT collapsed
        else:
            confirmed += 1
            continue
        if cls != "FENCE" and fence:
            cls = cls              # already surfacing; the fence is printed on the row
        surfaced.append({"class": cls, "id": ch["id"], "challenge": ch, "claim": cl,
                         "fence": fence})

    for cl in claims:
        if cl["id"] in answered:
            continue
        surfaced.append({"class": "UNCHALLENGED", "id": cl["id"], "challenge": None,
                         "claim": cl, "fence": cl.get("fence", "")})

    surfaced.sort(key=lambda r: (ORDER.index(r["class"]), r["id"]))
    return surfaced, confirmed, inconsistent


def render(surfaced, confirmed, inconsistent, claims, challenges, residual, paths):
    """The generated diff, as markdown text. WRITE-ONCE: this is derived, never hand-kept."""
    L = []
    counts = {}
    for r in surfaced:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    L.append("# PM-wave join — generated by `_join_claim_tables.py`")
    L.append("")
    L.append("*⛔ GENERATED. Do not hand-edit — edit the JSONL and re-run (write-once, ADR-0017).*")
    L.append("")
    L.append("**Sources:** `%s` (%d claim row(s)) · `%s` (%d challenge row(s))"
             % (paths[0], len(claims), paths[1], len(challenges)))
    L.append("")
    L.append("**Verdict tally (parsed rows only):** " + " · ".join(
        "%s %d" % (v, sum(1 for c in challenges if c["verdict"] == v))
        for v in CT.VERDICTS))
    L.append("")
    L.append("**CONFIRMED, unfenced, matched — collapsed to a count: %d.** "
             "Surfaced rows: %d (%s)."
             % (confirmed, len(surfaced),
                " · ".join("%s %d" % (k, counts[k]) for k in ORDER if k in counts) or "none"))
    if residual:
        L.append("")
        L.append("⛔ **RESIDUAL %d unparsed row(s) — the numbers above describe the PARSED "
                 "subset only.**" % residual)
    if inconsistent:
        L.append("")
        L.append("## ⛔ LOUD INCONSISTENCIES — the join refuses to reclassify these silently")
        L.append("")
        for m in inconsistent:
            L.append("- " + m)
    for cls in ORDER:
        rows = [r for r in surfaced if r["class"] == cls]
        if not rows:
            continue
        L.append("")
        L.append("## %s — %d" % (cls, len(rows)))
        L.append("")
        L.append("| id | claim | tag | verdict | evidence | fence / note |")
        L.append("|---|---|---|---|---|---|")
        for r in rows:
            cl, ch = r["claim"], r["challenge"]
            note = " ".join(x for x in [
                ("⛔ FENCE: " + r["fence"]) if r["fence"] else "",
                (ch or {}).get("note", ""), (cl or {}).get("note", "")] if x)
            L.append("| `%s` | %s | %s | %s | %s | %s |" % (
                r["id"],
                _cell((ch or cl).get("claim", "")),
                (cl or {}).get("tag", "—"),
                (ch or {}).get("verdict", "— (no challenge row)"),
                _cell((ch or cl).get("evidence", "")),
                _cell(note) or "—"))
    L.append("")
    return "\n".join(L)


def _cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def main(argv):
    consumed = {argv[i + 1] for i, a in enumerate(argv) if a == "--md" and i + 1 < len(argv)}
    args = [a for a in argv if not a.startswith("--") and a not in consumed]
    if len(args) != 2:
        sys.stderr.write("✖ REFUSED: need exactly <claims.jsonl> <challenges.jsonl>; got %r\n"
                         "  (%s --help for the contract)\n" % (args, os.path.basename(__file__)))
        return 2
    cpath, hpath = args
    claims, cdef = CT.load(cpath, expect_kind="claim")
    challenges, hdef = CT.load(hpath, expect_kind="challenge")
    residual = CT.report_defects(cdef, cpath) + CT.report_defects(hdef, hpath)

    surfaced, confirmed, inconsistent = join(claims, challenges)
    text = render(surfaced, confirmed, inconsistent, claims, challenges, residual, (cpath, hpath))
    print(text)
    if "--md" in argv:
        out = argv[argv.index("--md") + 1]
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote %s" % out, file=sys.stderr)
    if residual or inconsistent:
        print("\n⛔ JOIN rc=1 — %d unparsed row(s), %d loud inconsistency(ies)."
              % (residual, len(inconsistent)))
        return 1
    return 0


# ---- selftest: plant-then-detect BOTH directions + a SUPPRESSION ARM ---------------------------

def _c(i, **kw):
    return dict({"id": i, "kind": "claim", "claim": "c" + i, "evidence": "`ls` -> rc=0",
                 "tag": "PROVEN", "_src": "<mem>", "_lineno": 0}, **kw)


def _h(i, v, **kw):
    return dict({"id": i, "kind": "challenge", "claim": "h" + i, "evidence": "`ls` -> rc=0",
                 "verdict": v, "_src": "<mem>", "_lineno": 0}, **kw)


def selftest():
    fails = []

    # --- SUPPRESSION ARM: four rows a naive join would hide. Each MUST surface. ---
    claims = [_c("S-1"), _c("S-2"), _c("S-3", fence="declared stop: gate rewrites a tracked audit"),
              _c("S-4")]
    challenges = [_h("S-1", "CONTRADICTED"), _h("S-2", "CONFIRMED"),
                  _h("S-3", "CONFIRMED"), _h("N-9", "NEW")]
    surfaced, confirmed, inconsistent = join(claims, challenges)
    got = {r["id"]: r["class"] for r in surfaced}
    expect = {"S-1": "DISAGREEMENT", "S-3": "FENCE", "N-9": "NEW", "S-4": "UNCHALLENGED"}
    for k, v in expect.items():
        if got.get(k) != v:
            fails.append("SUPPRESSION: %s should surface as %s, got %r — a hidden row is a "
                         "decision nobody made" % (k, v, got.get(k)))
        else:
            print("  ✅ suppression arm: %s surfaces as %s" % (k, v))
    if confirmed != 1:
        fails.append("SUPPRESSION: CONFIRMED count %d, expected 1 (only the plain S-2 collapses)"
                     % confirmed)
    else:
        print("  ✅ suppression arm: exactly ONE row collapsed into the CONFIRMED count "
              "(the fenced CONFIRMED did not)")
    if "S-2" in got:
        fails.append("COLLAPSE BROKEN: a plain CONFIRMED row surfaced — the diff would be noise")
    else:
        print("  ✅ collapse works: the plain CONFIRMED row is a count, not a row")
    if inconsistent:
        fails.append("FALSE INCONSISTENCY on a clean fixture: %s" % inconsistent)

    # --- direction 1: PLANT the two loud inconsistencies ---
    _, _, inc = join([_c("P-1")], [_h("P-1", "NEW")])
    if not inc:
        fails.append("PLANT NOT CAUGHT: verdict=NEW on a matched id")
    else:
        print("  ✅ plant caught: verdict=NEW on a matched id is loud")
    _, _, inc = join([_c("P-1")], [_h("P-2", "CONFIRMED")])
    if not inc:
        fails.append("PLANT NOT CAUGHT: unmatched challenge row not marked NEW")
    else:
        print("  ✅ plant caught: unmatched challenge row not marked NEW is loud")

    # --- direction 2: REMOVE the defects — the same shape MUST go green ---
    surfaced, confirmed, inc = join([_c("P-1")], [_h("P-1", "CONFIRMED")])
    if inc or surfaced or confirmed != 1:
        fails.append("REMOVAL NOT GREEN: clean pair gave surfaced=%r inconsistent=%r confirmed=%d"
                     % ([r["id"] for r in surfaced], inc, confirmed))
    else:
        print("  ✅ removal green: the repaired pair joins to 1 CONFIRMED, 0 surfaced, 0 loud")

    # --- parse residual must reach the caller, not be swallowed ---
    import tempfile
    tmp = tempfile.mkdtemp(prefix="join-selftest-")
    good = os.path.join(tmp, "c.jsonl")
    bad = os.path.join(tmp, "h.jsonl")
    open(good, "w").write(json.dumps({"id": "R-1", "kind": "claim", "claim": "x",
                                      "evidence": "`ls`", "tag": "PROVEN"}) + "\n")
    open(bad, "w").write('{"id": "R-1", "kind": "challenge", BROKEN\n')
    rc = main([good, bad])
    if rc != 1:
        fails.append("RESIDUAL SWALLOWED: an unparseable challenge file returned rc=%d, not 1" % rc)
    else:
        print("  ✅ residual arm: an unparseable row makes the join rc=1, loudly")

    if fails:
        print("⛔ _join_claim_tables selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _join_claim_tables selftest PASS — suppression arm proves the four hideable classes "
          "surface; both plants caught; their removal goes green.")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
