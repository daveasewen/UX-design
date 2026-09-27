#!/usr/bin/env python3
"""wire_kg_generators.py [REPO_ROOT] [--check] — #304 W5c: wire the two KG generators' --check and
--selftest into knowledge/_build_all.py (STEPS + ROUTE_ROWS), beside the KG edge gate they belong with.

V2 (#304) named gen_kg_tokens.py UNWIRED; gen_kg_titles.py is born this wave. Four steps, four GATE
route rows. Idempotent: a second run changes nothing. REFUSES (exit 2, writes nothing) unless each
anchor occurs exactly once — so it cannot land on a _build_all.py another seat has reshaped without
someone looking. --check: exit 0 if already wired, 1 if not, 2 if the anchors are not there."""
import os, sys
if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = os.path.abspath(args[0]) if args else os.getcwd()
p = os.path.join(root, "knowledge", "_build_all.py")
s = open(p, encoding="utf-8").read()
STEP_ANCHOR = '    ("KG edge gate selftest (6 bites)", "_validate_kg.py", ["--selftest"]),\n'
STEP_ADD = (
    '    # #304 W5c — the KG generators\' drift checks, wired beside the KG edge gate. V2 (#304) named\n'
    '    # gen_kg_tokens.py UNWIRED (the [[unwired-validators-are-a-class]] shape: its only reader was\n'
    '    # the explorer build); gen_kg_titles.py is born #304 W5c. Each --check recomputes from the\n'
    '    # tree and compares bytes, so a ruling inscribed or a meta\'s tokens moved without the regen\n'
    '    # serial\'s `--write` / `--land` goes red here instead of going stale silently.\n'
    '    ("KG token-group generator drift check — _token_nodes.json vs the metas (s277-D12, wired #304 W5c)",\n'
    '     "gen_kg_tokens.py", ["--check"]),\n'
    '    ("KG token-group generator selftest — 8 bites (s277-D12)", "gen_kg_tokens.py", ["--selftest"]),\n'
    '    ("KG node-title generator drift check — _node_titles.json vs the records (#304 W5c)",\n'
    '     "gen_kg_titles.py", ["--check"]),\n'
    '    ("KG node-title generator selftest — 12 bites (#304 W5c)", "gen_kg_titles.py", ["--selftest"]),\n')
ROUTE_ANCHOR = ('    ("KG edge gate selftest (6 bites)", GATE,\n'
                '     "\\n❌ KG edge gate selftest failed (exit {code}) — python3 knowledge/_validate_kg.py --selftest"),\n')
ROUTE_ADD = (
    '    ("KG token-group generator drift check — _token_nodes.json vs the metas (s277-D12, wired #304 W5c)", GATE,\n'
    '     "\\n❌ KG token-group generator is STALE (exit {code}) — a meta\'s tokens block or the tier map moved under _token_nodes.json. Run: python3 knowledge/gen_kg_tokens.py --land --ratified s277-D12"),\n'
    '    ("KG token-group generator selftest — 8 bites (s277-D12)", GATE,\n'
    '     "\\n❌ KG token-group generator selftest failed (exit {code}) — python3 knowledge/gen_kg_tokens.py --selftest"),\n'
    '    ("KG node-title generator drift check — _node_titles.json vs the records (#304 W5c)", GATE,\n'
    '     "\\n❌ KG node titles are STALE (exit {code}) — a ruling or rule text moved under _node_titles.json (an inscription adds one). Run: python3 knowledge/gen_kg_titles.py --write"),\n'
    '    ("KG node-title generator selftest — 12 bites (#304 W5c)", GATE,\n'
    '     "\\n❌ KG node-title generator selftest failed (exit {code}) — python3 knowledge/gen_kg_titles.py --selftest"),\n')
wired = STEP_ADD in s and ROUTE_ADD in s
if wired:
    print("wire_kg_generators: already wired — nothing to do"); sys.exit(0)
if "--check" in sys.argv:
    print("wire_kg_generators --check: NOT wired"); sys.exit(1)
if s.count(STEP_ANCHOR) != 1 or s.count(ROUTE_ANCHOR) != 1 or STEP_ADD in s or ROUTE_ADD in s:
    print("wire_kg_generators: REFUSED — anchors found %d/%d times (need 1/1) or a half-wired state; nothing written"
          % (s.count(STEP_ANCHOR), s.count(ROUTE_ANCHOR))); sys.exit(2)
s = s.replace(STEP_ANCHOR, STEP_ANCHOR + STEP_ADD).replace(ROUTE_ANCHOR, ROUTE_ANCHOR + ROUTE_ADD)
open(p, "w", encoding="utf-8").write(s)
print("wire_kg_generators: wired 4 steps + 4 GATE routes into knowledge/_build_all.py")
