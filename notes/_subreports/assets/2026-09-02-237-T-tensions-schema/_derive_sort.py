#!/usr/bin/env python3
"""#237-T — DERIVE the tension sort. Every bucket is a printed rule over tensions.json.
A hand-sorted list is the defect (brief METHOD RULES). Read-only over the repo;
writes ONLY into this lane's own assets directory.

RULES, in precedence order:
  R-OBLIGATION : at least one party of the tension resolves to a principle-register row
                 whose grade == "L". By s237-D1 grade L is renamed OBLIGATION and by
                 s237-D2 it is a NODE TYPE no principle can outrank. Precedence: FIRST.
  R-RESOLVED   : the how_it_resolves prose cites at least one ruling id matching
                 ^s\\d+-D\\d+$ AND that id is present in knowledge/_rulings.json.
  R-OPEN       : everything else. (Complement; no membership test of its own.)

Cross-check X-LITERAL: independently of the register, does any party STRING carry a
literal obligation token (wcag|dsa|fca|eaa|en 301 549|gdpr|eu \\d|article)? Disagreement
between R-OBLIGATION and X-LITERAL is printed, never smoothed.
"""
import json, re, os, sys

REPO = "/sessions/dreamy-relaxed-noether/mnt/UX-design"
ASSETS = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-237-T-tensions-schema")
R1 = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-236-R1-principles-survey")

tensions = json.load(open(os.path.join(R1, "tensions.json")))["tensions"]
preg = json.load(open(os.path.join(R1, "principle-register.json")))["principles"]
rulings = json.load(open(os.path.join(REPO, "knowledge/_rulings.json")))["rulings"]

GRADE = {p["id"]: p["grade"] for p in preg}
RULING = {r["id"]: r for r in rulings}

PR_ID = re.compile(r"\bpr-[a-z0-9][a-z0-9-]*", re.I)
RULING_ID = re.compile(r"\bs\d+-D\d+\b")
LITERAL_OBL = re.compile(r"\b(wcag|dsa|fca|eaa|en[ -]?301[ -]?549|gdpr|article \d+)\b", re.I)


def parties(t):
    """Party STRINGS of a tension: side_a, side_b, side_c (nulls dropped)."""
    return [t[k] for k in ("side_a", "side_b", "side_c") if t.get(k)]


def party_ids(t):
    """pr- ids mentioned in the party strings, trimmed of trailing punctuation."""
    out = []
    for s in parties(t):
        for m in PR_ID.findall(s):
            out.append(m.rstrip("-.,;:").lower())
    return out


rows, unresolved_ids, disagreements = [], set(), []
for t in tensions:
    ids = party_ids(t)
    for i in ids:
        if i not in GRADE:
            unresolved_ids.add((t["id"], i))
    obl_ids = [i for i in ids if GRADE.get(i) == "L"]
    r_obligation = bool(obl_ids)

    cited = [c for c in RULING_ID.findall(t.get("how_it_resolves") or "")]
    cited_present = [c for c in cited if c in RULING]
    cited_absent = [c for c in cited if c not in RULING]
    r_resolved = bool(cited_present)

    x_literal = [s for s in parties(t) if LITERAL_OBL.search(s)]
    if bool(x_literal) != r_obligation:
        disagreements.append((t["id"], r_obligation, bool(x_literal), x_literal))

    if r_obligation:
        bucket = "settled-by-obligation"
    elif r_resolved:
        bucket = "resolved-here"
    else:
        bucket = "open"

    rows.append({
        "id": t["id"],
        "bucket": bucket,
        "party_ids": ids,
        "obligation_party_ids": obl_ids,
        "obligation_party_grades": {i: GRADE.get(i, "NOT-IN-REGISTER") for i in ids},
        "cited_ruling_ids_present": cited_present,
        "cited_ruling_ids_absent": cited_absent,
        "also_cites_ruling": bool(cited_present),   # for the triple/overlap report
        "x_literal_obligation_party": x_literal,
        "mediating_variable": t["mediating_variable"],
        "the_pull": t["the_pull"],
        "how_it_resolves": t["how_it_resolves"],
        "apollo_touch": t.get("apollo_touch"),
        "n_parties": len(parties(t)),
        "is_triple": bool(t.get("side_c")),
    })

counts = {}
for r in rows:
    counts[r["bucket"]] = counts.get(r["bucket"], 0) + 1

print("=" * 74)
print("RULE R-OBLIGATION : >=1 party id has principle-register grade 'L' (= OBLIGATION,")
print("                    s237-D1) -> bucket 'settled-by-obligation'. PRECEDENCE FIRST")
print("                    (s237-D2: no principle can outrank an obligation).")
print("RULE R-RESOLVED   : how_it_resolves cites s<N>-D<N> present in _rulings.json")
print("                    -> bucket 'resolved-here'.")
print("RULE R-OPEN       : complement of the two above.")
print("=" * 74)
for b in ("settled-by-obligation", "resolved-here", "open"):
    ids = [r["id"] for r in rows if r["bucket"] == b]
    print(f"{b:24s} n={counts.get(b,0):2d}  {', '.join(ids)}")
print("TOTAL", len(rows))

print("\n--- OVERLAP: obligation-bucket rows that ALSO cite a ruling (obligation wins) ---")
for r in rows:
    if r["bucket"] == "settled-by-obligation" and r["cited_ruling_ids_present"]:
        print(" ", r["id"], "obligation parties", r["obligation_party_ids"],
              "+ cites", r["cited_ruling_ids_present"])

print("\n--- TRIPLES (side_c present) ---")
for r in rows:
    if r["is_triple"]:
        print(" ", r["id"], r["bucket"], "parties:", r["n_parties"])

print("\n--- PARTY IDS NOT IN THE PRINCIPLE REGISTER (probe, not a defect claim) ---")
for tid, i in sorted(unresolved_ids):
    print(" ", tid, i)
print("  count:", len(unresolved_ids))

print("\n--- CITED RULING IDS ABSENT FROM _rulings.json ---")
any_absent = False
for r in rows:
    if r["cited_ruling_ids_absent"]:
        any_absent = True
        print(" ", r["id"], r["cited_ruling_ids_absent"])
if not any_absent:
    print("  none — every cited id resolves.")

print("\n--- X-LITERAL DISAGREEMENTS (register grade vs literal token in party string) ---")
if not disagreements:
    print("  none — the two independent rules agree on all 30.")
for d in disagreements:
    print(" ", d[0], "R-OBLIGATION=", d[1], "X-LITERAL=", d[2], d[3])

print("\n--- QUOTED `ruled` LINE FOR EVERY CITED RULING (<=15 words) ---")
seen = set()
for r in rows:
    for c in r["cited_ruling_ids_present"]:
        if c in seen:
            continue
        seen.add(c)
        txt = re.sub(r"\s+", " ", RULING[c].get("ruled") or "")
        if txt.startswith("#"):
            txt = re.sub(r"\s+", " ", RULING[c].get("says") or txt)
        words = txt.split()
        print(f"  {c}: \"{' '.join(words[:15])}\"" + (" …" if len(words) > 15 else ""))

os.makedirs(ASSETS, exist_ok=True)
json.dump({
    "$description": "#237-T derived sort of R1's 30 tensions. Buckets are DERIVED by the "
                    "rules printed in _derive_sort.py, not hand-sorted. FLOATED: nothing here is ruled.",
    "generated": "2026-09-02",
    "lane": "237-T",
    "rules": {
        "R-OBLIGATION": "at least one party id has principle-register grade 'L' (OBLIGATION, s237-D1); precedence first (s237-D2)",
        "R-RESOLVED": "how_it_resolves cites an s<N>-D<N> id present in knowledge/_rulings.json",
        "R-OPEN": "complement",
    },
    "counts": counts,
    "rows": rows,
}, open(os.path.join(ASSETS, "tension-sort.json"), "w"), indent=1, ensure_ascii=False)
print("\nWROTE", os.path.join(ASSETS, "tension-sort.json"))
