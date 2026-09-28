# #306 W1 - meta-mutation: each mutant is the tool's source with ONE clause broken, run in memory
# (exec, __name__ != '__main__'), and its selftest must go RED. No file under knowledge/ is written.
import io, sys, contextlib, types
sys.path.insert(0, 'knowledge')
M = [
 ('_wrap_regen.py', '    ("knowledge/gen_kg_titles.py", ["--write"], ["--check"], ["knowledge/_node_titles.json"]),\n', '', 'titles dropped from the serial'),
 ('_wrap_carries.py', 'new_line = line[:a] + "~~" + title + "~~" + ins_note', 'new_line = line[:a] + title + ins_note', 'strike without ~~'),
 ('_wrap_carries.py', 'return s.replace("[\\x00", "[1")', 'return s.replace("[\\x00", "[0")', 'NEW not aged to 1'),
 ('_wrap_rows.py', 'f"born closed (s305-D40): {op[\'home\']} filed at #{n} — the file is the record."', '"born closed"', 'born-closed receipt without its home'),
 ('_wrap_commit.py', '    bad = [p for p in P if p not in ch]\n', '    bad = []\n', 'unchanged paths not refused'),
 ('_wrap_ops.py', '    roll = dps[1:]', '    roll = dps[2:]', '2d keeps 3 PRIOR'),
 ('_wrap_facts.py', '            if rec.get("isSidechain"):\n                continue\n', '', 'sidechain counted'),
]
for f, a, b, why in M:
    src = open('knowledge/' + f, encoding='utf-8').read()
    assert src.count(a) == 1, (f, why)
    mod = types.ModuleType('mut'); mod.__file__ = 'knowledge/' + f
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src.replace(a, b), f, 'exec'), mod.__dict__)
        try:
            rc = mod.selftest()
        except Exception as e:
            rc = f'raised {type(e).__name__}'
    red = [l.strip() for l in buf.getvalue().splitlines() if l.startswith('  ✗')]
    print(f'{f} [{why}] -> selftest rc {rc}; {len(red)} bite(s) red' + (f', first: {red[0][:90]}' if red else ''))
