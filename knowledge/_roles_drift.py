#!/usr/bin/env python3
"""_roles_drift.py — ROLES DRIFT, measured (#273). roles.json membership vs the metas' `provides`.

WHAT. `knowledge/roles.json` carries the RULED membership (s252-D1: the twelve roles "with the
membership … exactly as the v1 page lays them out"). A meta carries `provides: <role>` as an
ADDRESS into that file, and only a meta's `provides` generates a `providesRole` edge
(s270-D2, gen_kg_roles_desk.py). The first authoring pass covered 25 metas (s251-D12) and
said "wider scope is re-judged once that pass is done, not decided now". This script measures
how far the two homes are apart TODAY, per role, per meta, and what a second pass would touch.

READ-ONLY. Emits JSON (--json) or a plain table. Every figure a review page quotes about this
drift comes from here, never from a human reading (the s254-D2 item 2 principle).

  python3 knowledge/_roles_drift.py            # table
  python3 knowledge/_roles_drift.py --json     # machine-readable, for the review page builder
  python3 knowledge/_roles_drift.py --selftest # the counts are exercised on a synthetic corpus
"""
from __future__ import annotations
import argparse, glob, json, os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROLES = os.path.join(HERE, "roles.json")
COMP = os.path.join(HERE, "components")
WHENF = os.path.join(HERE, "when-fields.json")

EM_DASH = "—"
FIELD_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_.]*)\s*(=|!=|<=|>=|<|>|\bin\b)", re.I)


def load_metas(comp_dir: str) -> dict:
    metas = {}
    for f in sorted(glob.glob(os.path.join(comp_dir, "*.meta.json"))):
        stem = os.path.basename(f)[: -len(".meta.json")]
        if stem.startswith("EXAMPLE"):
            continue
        with open(f, encoding="utf-8") as fh:
            metas[stem] = json.load(fh)
    return metas


def gate_fields(when: str | None) -> list[str]:
    """Left-hand field names in the GATE half (before the first em-dash) of a `when`."""
    if not when or not isinstance(when, str):
        return []
    gate = when.split(EM_DASH, 1)[0]
    out = []
    for clause in re.split(r"\s+(?:AND|OR)\s+", gate):
        m = FIELD_RE.match(clause)
        if m:
            out.append(m.group(1))
    return out


def measure(roles_path=ROLES, comp_dir=COMP, whenf_path=WHENF) -> dict:
    roles = json.load(open(roles_path, encoding="utf-8"))
    metas = load_metas(comp_dir)
    legal = set(json.load(open(whenf_path, encoding="utf-8")).get("fields", {}).keys())
    nap = [s.strip().split(" ")[0] for s in roles.get("$not-a-provider", "").split("·")]

    per_role, total, agree, silent, contradict, dangling = [], 0, 0, 0, [], []
    silent_with_json_when = 0
    for slug, r in roles["roles"].items():
        provs = r.get("providers", [])
        rows = []
        for p in provs:
            ps = p["slug"] if isinstance(p, dict) else p
            jw = (p.get("when") if isinstance(p, dict) else None)
            m = metas.get(ps)
            mp = m.get("provides") if m else None
            state = ("no-meta-file" if m is None else
                     "agrees" if mp == slug else
                     "contradicts" if mp else "silent")
            total += 1
            if state == "agrees": agree += 1
            elif state == "silent":
                silent += 1
                if jw: silent_with_json_when += 1
            elif state == "contradicts": contradict.append((ps, slug, mp))
            elif state == "no-meta-file": dangling.append((ps, slug))
            mw = m.get("when") if m else None
            rows.append({"slug": ps, "state": state, "json_when": jw,
                         "meta_when": mw, "meta_priority": (m or {}).get("priority"),
                         "meta_shape": (m or {}).get("shape"), "meta_answers": (m or {}).get("answers"),
                         "illegal_fields": [f for f in gate_fields(mw) if f not in legal]})
        n_agree = sum(1 for x in rows if x["state"] == "agrees")
        per_role.append({"role": slug, "index": r.get("index"), "definition": r.get("definition"),
                         "axis": r.get("axis"), "json": len(rows), "meta_agrees": n_agree,
                         "meta_silent": sum(1 for x in rows if x["state"] == "silent"),
                         "json_when_present": sum(1 for x in rows if x["json_when"]),
                         "zero_in_metas": n_agree == 0, "providers": rows})

    # reverse direction: metas that declare a role roles.json does not list them under
    back = []
    for stem, m in metas.items():
        mp = m.get("provides")
        if not mp: continue
        listed = [(p["slug"] if isinstance(p, dict) else p)
                  for p in roles["roles"].get(mp, {}).get("providers", [])]
        if stem not in listed: back.append((stem, mp))
    unknown_role = [(s, m.get("provides")) for s, m in metas.items()
                    if m.get("provides") and m["provides"] not in roles["roles"]]
    nap_with_provides = [s for s in nap if s in metas and metas[s].get("provides")]

    # `when` field legality across the WHOLE library (the #272 inscription wrote 15 gates)
    when_metas = {s: m["when"] for s, m in metas.items() if isinstance(m.get("when"), str)}
    illegal = {s: [f for f in gate_fields(w) if f not in legal] for s, w in when_metas.items()}
    illegal = {s: f for s, f in illegal.items() if f}
    # the offending CLAUSE, per (meta, field) — so a review page never reads a meta as a second source
    illegal_clauses = []
    for s, fields in illegal.items():
        gate = when_metas[s].split(EM_DASH, 1)[0]
        clauses = re.split(r"\s+(?:AND|OR)\s+", gate)
        for f in fields:
            cl = next((c.strip() for c in clauses
                       if FIELD_RE.match(c) and FIELD_RE.match(c).group(1) == f), "")
            illegal_clauses.append({"meta": s, "field": f, "clause": cl,
                                    "is_provider": s in {p["slug"] for r in per_role for p in r["providers"]}})

    return {
        "measured_at": subprocess.run(["git", "log", "-1", "--format=%h %cs"], cwd=HERE,
                                      capture_output=True, text=True).stdout.strip(),
        "corpus_metas": len(metas), "roles": len(roles["roles"]),
        "memberships_json": total, "memberships_meta_agree": agree,
        "memberships_meta_silent": silent, "silent_with_json_when": silent_with_json_when,
        "contradictions": contradict, "dangling_slugs": dangling,
        "meta_provides_not_in_json": back, "meta_provides_unknown_role": unknown_role,
        "not_a_provider_with_provides": nap_with_provides,
        "roles_zero_in_metas": [r["role"] for r in per_role if r["zero_in_metas"]],
        "json_when_present": sum(r["json_when_present"] for r in per_role),
        "metas_with_when": len(when_metas), "metas_with_provides": sum(1 for m in metas.values() if m.get("provides")),
        "legal_when_fields": sorted(legal),
        "metas_with_illegal_when_fields": illegal,
        "illegal_when_clauses": illegal_clauses,
        "per_role": per_role,
    }


def table(d: dict) -> str:
    L = [f"ROLES DRIFT — measured at {d['measured_at']} · corpus {d['corpus_metas']} metas · {d['roles']} roles",
         f"  memberships  roles.json {d['memberships_json']} · metas agree {d['memberships_meta_agree']} · "
         f"metas silent {d['memberships_meta_silent']} (of which {d['silent_with_json_when']} carry a roles.json `when`)",
         f"  contradictions {len(d['contradictions'])} · dangling slugs {len(d['dangling_slugs'])} · "
         f"meta→role not in json {len(d['meta_provides_not_in_json'])} · unknown role {len(d['meta_provides_unknown_role'])} · "
         f"not-a-provider carrying provides {len(d['not_a_provider_with_provides'])}",
         f"  roles at ZERO in the metas: {', '.join(d['roles_zero_in_metas']) or 'none'}",
         f"  `when`: roles.json {d['json_when_present']}/{d['memberships_json']} · metas {d['metas_with_when']}/{d['corpus_metas']} · "
         f"metas whose gate uses a field OUTSIDE when-fields.json: {len(d['metas_with_illegal_when_fields'])}",
         "", f"  {'role':17} {'json':>4} {'agree':>5} {'silent':>6} {'j-when':>6}"]
    for r in d["per_role"]:
        L.append(f"  {r['role']:17} {r['json']:>4} {r['meta_agrees']:>5} {r['meta_silent']:>6} {r['json_when_present']:>6}"
                 + ("   ← ZERO in metas" if r["zero_in_metas"] else ""))
    if d["metas_with_illegal_when_fields"]:
        L.append("")
        L.append("  gate fields outside the closed list (s254-D2 item 2):")
        for s, f in sorted(d["metas_with_illegal_when_fields"].items()):
            L.append(f"    {s}: {', '.join(f)}")
    return "\n".join(L)


def selftest() -> int:
    import tempfile
    t = tempfile.mkdtemp()
    cd = os.path.join(t, "components"); os.mkdir(cd)
    json.dump({"roles": {"r1": {"providers": [{"slug": "a", "when": "x"}, {"slug": "b"}, {"slug": "ghost"}]},
                          "r2": {"providers": [{"slug": "c"}]}}, "$not-a-provider": "z"},
              open(os.path.join(t, "roles.json"), "w"))
    json.dump({"fields": {"shape": {}}}, open(os.path.join(t, "when-fields.json"), "w"))
    for stem, body in {"a": {"provides": "r1", "when": "shape = q AND steps >= 2 — prose"},
                       "b": {}, "c": {"provides": "r9"}, "z": {"provides": "r2"}}.items():
        json.dump(body, open(os.path.join(cd, f"{stem}.meta.json"), "w"))
    d = measure(os.path.join(t, "roles.json"), cd, os.path.join(t, "when-fields.json"))
    checks = [
        ("memberships_json", d["memberships_json"] == 4),
        ("agree", d["memberships_meta_agree"] == 1),
        ("silent", d["memberships_meta_silent"] == 1),
        ("silent_with_json_when", d["silent_with_json_when"] == 0),
        ("contradiction c", d["contradictions"] == [("c", "r2", "r9")]),
        ("dangling ghost", d["dangling_slugs"] == [("ghost", "r1")]),
        ("unknown role r9", d["meta_provides_unknown_role"] == [("c", "r9")]),
        ("back z→r2", ("z", "r2") in d["meta_provides_not_in_json"]),
        ("nap z", d["not_a_provider_with_provides"] == ["z"]),
        ("zero role r2", d["roles_zero_in_metas"] == ["r2"]),
        ("illegal field steps only", d["metas_with_illegal_when_fields"] == {"a": ["steps"]}),
        ("illegal clause carried", d["illegal_when_clauses"] ==
         [{"meta": "a", "field": "steps", "clause": "steps >= 2", "is_provider": True}]),
    ]
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    bad = [n for n, ok in checks if not ok]
    print(f"  {'✅' if not bad else '⛔'} {len(checks)-len(bad)}/{len(checks)}")
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    d = measure()
    print(json.dumps(d, indent=1, ensure_ascii=False) if a.json else table(d))
