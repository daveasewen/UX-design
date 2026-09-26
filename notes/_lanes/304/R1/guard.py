import ast, sys, os
root = sys.argv[1]
TOP = ["_bite_goal.py","_bite_kg_edge_proposal.py","_build_kg_explorer.py","_gen_ruling_edges_from_recs.py","_kg_history.py"]
RENDER = ["verify_demo_slides_268.py","verify_demo_slides_268_v3.py","verify_demo_slides_268_v5.py","verify_demo_slides_268_v6.py","verify_demo_slides_268_v7.py","verify_demo_slides_268_v74_gearbox.py","verify_demo_slides_268_v75_gearbox.py"]
PLAIN = "from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)  # help gate (#158 write-by-default class; guarded #304 R1)\n"
WALK = ('import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class; guarded #304 R1)\n'
        '_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))\n'
        'while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):\n'
        '    _hg_d = _hg_os.path.dirname(_hg_d)\n'
        '_hg_sys.path.insert(0, _hg_d)\n'
        'from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)\n')
for rel, guard in [("knowledge/"+f, PLAIN) for f in TOP] + [("knowledge/_render/"+f, WALK) for f in RENDER]:
    p = os.path.join(root, rel)
    src = open(p).read()
    if "_help_gate(" in src:
        print("already", rel); continue
    t = ast.parse(src)
    d = t.body[0]
    assert isinstance(d, ast.Expr) and isinstance(d.value, ast.Constant) and isinstance(d.value.value, str), rel
    lines = src.splitlines(keepends=True)
    end = d.end_lineno  # 1-based last line of docstring
    new = "".join(lines[:end]) + guard + "".join(lines[end:])
    ast.parse(new)
    open(p, "w").write(new)
    print("guarded", rel, "after line", end)
