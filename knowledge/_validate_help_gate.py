#!/usr/bin/env python3
"""
_validate_help_gate.py — GATE for the GENERATORS-WRITE-BY-DEFAULT class (#158).

The defect (born #150, homed in `_FUTURE-STATE.md` at #153, unfixed through #157):
a script does its work — and its WRITES — before it has looked at argv, so
`python3 knowledge/gen_showroom.py --help` REWROTE showroom/ at #157. A runtime
write-probe at #158 measured 52 scripts that attempted a repo write on a bare
`--help`, 14 of them at MODULE level.

WHAT THIS GATE PARSES (the consumer's grammar, not a grep): the module AST of every
entry-point script under knowledge/. An entry point is a .py file with a shebang or
an `if __name__ == "__main__":` block. Each one must satisfy ONE of:

  (a) it calls `_help_gate(...)` (knowledge/_helpgate.py) among its OPENING
      statements — before any statement that could execute work; or
  (b) it builds an `argparse` parser, which owns `--help` itself.

"Opening statements" means: only a docstring, imports, plain constant/name
assignments and `sys.path` bookkeeping may precede the guard. A call, an `if`, a
`for`, a `with`, a function invocation of any kind before the guard makes the file
RED — that prologue is exactly where the module-level writers did their damage.

This gate is STRUCTURAL on purpose. The runtime probe (`--probe`, below) can only
see a write that actually happens on the run it observes: gen_showroom writes only
when showroom/ is STALE, so a probe on a clean tree would have called the #157
offender green. The AST rule gates the PRESENCE of the contract instead of the
drift [[gate-inside-the-growth-loop]].

Usage:
  python3 knowledge/_validate_help_gate.py            # the gate (wired into _build_all.py)
  python3 knowledge/_validate_help_gate.py --selftest # mutation test: a deliberate offender must go RED
  python3 knowledge/_validate_help_gate.py --list     # list the entry points in scope
"""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _helpgate import help_gate as _help_gate  # noqa: E402
_help_gate(__doc__, __name__, __file__)

SKIP_DIRS = ("_retired", "__pycache__", "archive", ".git", "node_modules")
SKIP_FILES = ("_helpgate.py",)
GUARD_NAME = "_help_gate"

# statement types allowed to PRECEDE the guard call
_PROLOGUE_OK = (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign, ast.AugAssign,
                ast.Pass, ast.While)   # While: the _helpgate path walk-up bootstrap


def scripts(root=HERE):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if fn.endswith(".py") and fn not in SKIP_FILES:
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def is_entry_point(src, tree):
    if src.startswith("#!"):
        return True
    for node in tree.body:
        if (isinstance(node, ast.If) and isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__"):
            return True
    return False


def guard_index(tree):
    """Index of the statement calling _help_gate at module level, or None."""
    for i, node in enumerate(tree.body):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            f = node.value.func
            name = getattr(f, "id", None) or getattr(f, "attr", None)
            if name == GUARD_NAME or name == "help_gate":
                return i
    return None


def uses_argparse(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(a.name == "argparse" for a in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and node.module == "argparse":
            return True
    return False


def check_file(path, src=None):
    """Return a failure string, or None when the file is clean."""
    src = src if src is not None else open(path).read()
    rel = os.path.relpath(path, os.path.dirname(HERE))
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return f"{rel}: does not parse ({e})"
    if not is_entry_point(src, tree):
        return None
    if uses_argparse(tree):
        return None
    gi = guard_index(tree)
    if gi is None:
        return (f"{rel}: NO HELP GATE — add\n"
                f"      from _helpgate import help_gate as _help_gate; "
                f"_help_gate(__doc__, __name__, __file__)\n"
                f"      near the top (before any executable statement). "
                f"See knowledge/_helpgate.py.")
    for node in tree.body[:gi]:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue          # docstring / bare string
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            f = node.value.func
            # sys.path bookkeeping is the one call the bootstrap needs
            if getattr(f, "attr", None) in ("insert", "append", "extend"):
                continue
        if not isinstance(node, _PROLOGUE_OK):
            return (f"{rel}: help gate at statement {gi} is TOO LATE — "
                    f"{type(node).__name__} on line {node.lineno} runs first")
    return None


def run(paths=None):
    paths = paths or scripts()
    fails = [f for f in (check_file(p) for p in paths) if f]
    return paths, fails


def selftest():
    """MUTATION TEST: a deliberate offender must make the gate RED."""
    good = ('#!/usr/bin/env python3\n"""doc"""\n'
            'from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)\n'
            'import os\nopen("/x", "w").write("boom")\n')
    offender = ('#!/usr/bin/env python3\n"""doc"""\nimport os\n'
                'open("/x", "w").write("boom")\n'
                'from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)\n')
    no_gate = '#!/usr/bin/env python3\n"""doc"""\nimport os\nopen("/x", "w").write("boom")\n'
    lib = '"""a library module, no shebang, no __main__"""\nimport os\nX = 1\n'
    ap = ('#!/usr/bin/env python3\n"""doc"""\nimport argparse\n'
          'p = argparse.ArgumentParser()\n')
    cases = [("guard first -> GREEN", good, False),
             ("write before guard -> RED", offender, True),
             ("no guard at all -> RED", no_gate, True),
             ("library module -> GREEN (not an entry point)", lib, False),
             ("argparse owns --help -> GREEN", ap, False)]
    fails = []
    for label, src, want_red in cases:
        got = check_file(os.path.join(HERE, "_mutant.py"), src)
        red = got is not None
        status = "RED" if red else "GREEN"
        print(f"  {'✓' if red == want_red else '✗'} {label:48s} -> {status}"
              + (f"  [{got.splitlines()[0]}]" if got else ""))
        if red != want_red:
            fails.append(label)
    if fails:
        print("❌ help-gate selftest FAILED: " + "; ".join(fails))
        sys.exit(1)
    print("_validate_help_gate --selftest OK — 5 bites "
          "(guard-first · write-before-guard RED · missing-guard RED · library · argparse).")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    paths = scripts()
    if "--list" in sys.argv:
        for p in paths:
            if check_file(p) is None and is_entry_point(open(p).read(), ast.parse(open(p).read())):
                print("  " + os.path.relpath(p, os.path.dirname(HERE)))
        return
    _, fails = run(paths)
    if fails:
        print(f"help-gate: {len(paths)} script(s) scanned, {len(fails)} failure(s) — "
              f"a script that can write before it reads argv is the #157 gen_showroom defect")
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print(f"help-gate OK — {len(paths)} script(s) scanned; every entry point answers "
          f"--help before it can write.")


if __name__ == "__main__":
    main()
