#!/usr/bin/env python3
"""C0 gate runner: the meta-reading gates, non-writing modes only. Usage: gates.py <tag> <i:j>"""
import subprocess, sys, json, time, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
G = [
 ["_probe_registry/probe_meta_schema.py", "--check"],
 ["_probe_registry/probe_meta_schema.py", "--selftest"],
 ["_validate_kg.py"], ["_validate_kg.py", "--selftest"],
 ["gen_kg_sources.py", "--check"], ["gen_kg_sources.py", "--selftest"],
 ["_validate_binds_ratchet.py"], ["_validate_binds_resolve.py"],
 ["_validate_intent_resolve.py"], ["_validate_roles_resolve.py"], ["_validate_roles_resolve.py", "--selftest"],
 ["_validate_edges.py", "--check"], ["_validate_edges.py", "--selftest"],
 ["gen_kg_titles.py", "--check"], ["gen_kg_tokens.py", "--check"],
 ["tokens/_build_blast_radius.py", "--check"], ["gen_component_partials.py", "--check"],
 ["_validate_palette_tier.py"], ["_build_memento_index.py", "--check"], ["gen_itinerary_status.py", "--check"],
 ["_consult.py", "--selftest"], ["gen_dashboard.py", "--check"],
 ["_tests/test_gates.py"],
]
tag, rng = sys.argv[1], sys.argv[2]
i, j = [int(x) for x in rng.split(":")]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gates-%s.jsonl" % tag)
for g in G[i:j]:
    t = time.time()
    try:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "knowledge", g[0])] + g[1:], cwd=ROOT,
                           capture_output=True, text=True, timeout=170)
        rc, tail = p.returncode, [l for l in (p.stdout + p.stderr).strip().splitlines() if l.strip()][-2:]
    except subprocess.TimeoutExpired:
        rc, tail = "TIMEOUT", []
    row = {"gate": " ".join(g), "rc": rc, "s": round(time.time() - t, 1), "tail": [x[:220] for x in tail]}
    open(out, "a").write(json.dumps(row, ensure_ascii=False) + "\n")
    print(row["rc"], row["s"], row["gate"], "|", " / ".join(row["tail"])[:300])
