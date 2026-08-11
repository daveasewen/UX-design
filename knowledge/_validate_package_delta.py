#!/usr/bin/env python3
"""memento-package delta-audit gate — enforces Dave's #64 boundary ruling (#79 build).

WHY THIS EXISTS. `memento-package/_PACKAGE-SPEC.md:13-14`, Dave's #64 ruling: "Nothing in
Apollo reads it; no Apollo gate globs it; no Apollo file MOVES into it — copies only, and
every copy is delta-audited." The rule existed with nothing built to enforce it, and
`_gen_chain.py` silently regressed 54 lines behind `knowledge/_gen_chain.py` (the #73
title-block + stale-title refusal) in BOTH in-package copies, undetected, until #79 measured
it. This gate is the enforcement the ruling always implied.

FOUR ARMS.
  1. VERBATIM SET — `_gen_chain.py` / `_memento_search.py` / `_search_core.py` / `_graph_edges.py` must be
     byte-identical to their `knowledge/` originals, in BOTH package copies.
  2. THE SHIM — `_capture_gate.py` in the package is NOT a copy, by design (its own
     docstring: a purpose-written standalone shim reproducing four functions' behaviour).
     It is exempt from wholesale comparison. Instead this honours its DECLARED PROVENANCE:
     the shim's docstring names the exact functions/constants it says it ported and the
     commit each chain was ported from. Two chains, both declared in the shim's own
     docstring:
       (a) `knowledge/_capture_gate.py` @ commit c853b0a (re-ported #114; was 91d7528) — chain_parts, read_chain_tk,
           measure_tokens, measurement_degraded, dofirst_index, _heal_tiktoken, plus the
           six named constants (BYTES_PER_TOKEN, DOFIRST_ITEM_RE, DOFIRST_HOOK_MAX,
           DOFIRST_INDEX_TK_MAX, LS_DELTA_RE, _TIKTOKEN_HEAL_TRIED).
       (b) `knowledge/_gm_usage.py` @ commit ace3ed3 — GM_VOCAB, LS_VOCAB (the shim's own
           docstring flags this as "A DEPENDENCY THE MANIFEST DID NOT NAME").
  3. CROSS-COPY IDENTITY — every file in `machinery/` must be byte-identical to its
     namesake in `claude-plugin/memento/machinery/`, in both directions, PLUS both copies
     must together carry every file on the known-files list (catches the case where a file
     vanishes from BOTH copies at once, which the pairwise check alone would miss).
  4. UNKNOWN FILES — any file in either machinery folder not on the known-files list FAILS
     LOUD, named. `__pycache__/` is the one deliberate, NAMED exclusion (gitignored
     Python bytecode cache, not shipped content — see .gitignore:8-9). Project rule: a gate
     that enumerates rather than failing loud on the unknown is the scope-blindness defect;
     this is the allowlist-with-loud-unknown shape, not a silent ignore-list.

METHOD PROOF FOR ARM 2 — why AST source-segment hashing, not `git log -L` or line ranges.
Measured at #79: `knowledge/_capture_gate.py` grew from ~2,500 lines (port time) to 4,321
lines across FOUR commits after the port (514f4bd, f8ff234, 9cde313, 4661333) — so the
docstring's own line numbers (e.g. "measure_tokens lines 1350-1374") no longer address the
right text; a line-range diff would silently compare the WRONG code. AST extraction finds
each function/assignment BY NAME in both the historical git blob and the current file and
hashes only ITS OWN source text (`ast.get_source_segment`, Python's own span-getter) — immune
to unrelated edits moving the function up or down the file. Proven, this session: the same
extraction run against the real repo found chain (a)'s 12 names and chain (b)'s 2 names all
byte-identical between their port commits and HEAD, despite the surrounding files changing
substantially — i.e. the method correctly stayed GREEN on real, heavy, UNRELATED drift, which
a whole-file hash could never have distinguished from a real break.

GATE-GLOB-SCOPE: this gate globs `memento-package/` explicitly and ONLY (plus reads, never
writes, `knowledge/_gen_chain.py` / `_memento_search.py` / `_search_core.py` / `_graph_edges.py`
/ `_capture_gate.py` / `_gm_usage.py` as comparison SOURCES). It does not touch, read the content of for grading, or
widen any other gate's glob (gate-glob-scope-rule).

USAGE
    python3 knowledge/_validate_package_delta.py              # run the gate
    python3 knowledge/_validate_package_delta.py --selftest   # the bites, mutation-tested
"""
import ast
import difflib
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

COPY_A = "memento-package/machinery"
COPY_B = "memento-package/claude-plugin/memento/machinery"
SHIM_NAME = "_capture_gate.py"

# s124: _graph_edges.py joined the set — the #115 sync made _memento_search.py import it, and a
# green audit over a copy with a dead import is the no-gate-parses-the-artefact class (#122).
# Its data files (_decision-graph.json etc.) deliberately do NOT ship: _graph_edges degrades
# loud-and-named via available()/unavailable_notice() when they're absent.
VERBATIM_SET = ("_gen_chain.py", "_memento_search.py", "_search_core.py", "_graph_edges.py")
KNOWN_FILES = set(VERBATIM_SET) | {SHIM_NAME, "_consult-lexicon.json", "_MACHINERY-MANIFEST.md"}
# ⚠ NAMED, deliberate, narrow exclusion — NOT a blanket ignore-list. __pycache__ is Python's
# own bytecode cache, gitignored (.gitignore:8 `__pycache__/`, :9 `*.pyc`), regenerates on
# every run, and carries no shipped content. Excluding it by name is the allowlist doing its
# job; a gate that silently widened this pattern would be the scope-blindness defect instead.
IGNORE_DIRS = {"__pycache__"}

# ---- Provenance chain (a): knowledge/_capture_gate.py @ c853b0a -------------------------
PORT_COMMIT_A = "9dcf62d"   # ★ #149 RE-PORT: chain_parts had drifted since c853b0a
# (the s125-D1 {{BUILD_VERDICT}} splice). Re-reviewed and re-ported into the shim, the shim's
# docstring now declares this commit, and this constant follows it.
# ★ #114 RE-PORT: measure_tokens / measurement_degraded /
# DOFIRST_INDEX_TK_MAX had drifted since 91d7528 (the #82-D1 three-tier cascade, and the
# constant's 700). All three were re-reviewed and re-ported into the shim, the shim's docstring
# now declares this commit, and this constant follows it — the gate's own remedy path ("the shim
# was re-ported and the gate was not updated to match"). ⚠ No VALUE was changed by the sync:
# DOFIRST_INDEX_TK_MAX is 700 on BOTH sides (Dave's, #111-D4).
SHIM_SOURCE_FILE_A = "knowledge/_capture_gate.py"
PORTED_FUNCS_A = ("chain_parts", "read_chain_tk", "measure_tokens", "measurement_degraded",
                  "dofirst_index", "_heal_tiktoken")
PORTED_CONSTS_A = ("BYTES_PER_TOKEN", "DOFIRST_ITEM_RE", "DOFIRST_HOOK_MAX",
                   "DOFIRST_INDEX_TK_MAX", "LS_DELTA_RE", "_TIKTOKEN_HEAL_TRIED")

# ---- Provenance chain (b): knowledge/_gm_usage.py @ ace3ed3 ------------------------------
PORT_COMMIT_B = "ace3ed3"
SHIM_SOURCE_FILE_B = "knowledge/_gm_usage.py"
PORTED_CONSTS_B = ("GM_VOCAB", "LS_VOCAB")

DOCSTRING_COMMIT_RE_A = re.compile(r"Ported from `knowledge/_capture_gate\.py` @ HEAD `([0-9a-f]{7,40})`")
DOCSTRING_COMMIT_RE_B = re.compile(r"`knowledge/_gm_usage\.py` @ HEAD `([0-9a-f]{7,40})`")


# ------------------------------------------------------------------------------ helpers
def _diff_line_count(a_text, b_text):
    """Count of changed lines (added + removed, unified-diff style) between two texts."""
    a_lines = a_text.splitlines(keepends=True)
    b_lines = b_text.splitlines(keepends=True)
    diff = list(difflib.unified_diff(a_lines, b_lines, n=0))
    return sum(1 for ln in diff
               if (ln.startswith("+") or ln.startswith("-"))
               and not ln.startswith("+++") and not ln.startswith("---"))


def _walk_files(dirpath):
    """Relative file paths inside dirpath, recursive, excluding IGNORE_DIRS BY NAME."""
    out = set()
    for root, dirs, files in os.walk(dirpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            out.add(os.path.relpath(os.path.join(root, f), dirpath))
    return out


def _find_node(tree, name):
    """The module-level FunctionDef/AsyncFunctionDef or Assign(-target) node named `name`."""
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name:
            return n
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name
                                              for t in n.targets):
            return n
    return None


def extract_named(source_text, names):
    """{name: source_segment_text} for every name in `names` found at module level.
    Missing names are simply absent from the returned dict — callers must check."""
    tree = ast.parse(source_text)
    out = {}
    for name in names:
        node = _find_node(tree, name)
        if node is not None:
            out[name] = ast.get_source_segment(source_text, node)
    return out


def _git_show(git_root, commit, relpath):
    """(text, None) or (None, error). Pure read of the object database — touches no
    working-tree file and no index, so this is safe to point at the REAL repo even
    during a mutation test (nothing in the real repo is written or mutated by this call)."""
    r = subprocess.run(["git", "show", f"{commit}:{relpath}"], cwd=git_root,
                        capture_output=True, text=True)
    if r.returncode != 0:
        err = (r.stderr or "").strip() or f"git show {commit}:{relpath} failed (exit {r.returncode})"
        return None, err
    return r.stdout, None


# ------------------------------------------------------------------------- arm 1: VERBATIM SET
def check_verbatim_set(repo):
    fails = []
    for fname in VERBATIM_SET:
        src = os.path.join(repo, "knowledge", fname)
        if not os.path.isfile(src):
            fails.append(f"VERBATIM SET: source knowledge/{fname} does not exist — cannot audit")
            continue
        src_bytes = open(src, "rb").read()
        for copy_label, copy_rel in (("machinery/", COPY_A), ("claude-plugin copy", COPY_B)):
            dst = os.path.join(repo, copy_rel, fname)
            if not os.path.isfile(dst):
                fails.append(f"VERBATIM SET: {fname} is MISSING from {copy_label} "
                             f"({copy_rel}/{fname})")
                continue
            dst_bytes = open(dst, "rb").read()
            if dst_bytes != src_bytes:
                dl = _diff_line_count(src_bytes.decode("utf-8", "replace"),
                                       dst_bytes.decode("utf-8", "replace"))
                fails.append(
                    f"VERBATIM SET: {copy_rel}/{fname} DIFFERS from knowledge/{fname} "
                    f"(copy={copy_label} file={fname}) — {dl} line(s) differ "
                    f"(sha256 {hashlib.sha256(dst_bytes).hexdigest()[:12]} vs source "
                    f"{hashlib.sha256(src_bytes).hexdigest()[:12]})")
    return fails


# --------------------------------------------------------------------- arm 3: CROSS-COPY
def check_cross_copy_identity(repo):
    fails = []
    dir_a = os.path.join(repo, COPY_A)
    dir_b = os.path.join(repo, COPY_B)
    files_a = _walk_files(dir_a) if os.path.isdir(dir_a) else set()
    files_b = _walk_files(dir_b) if os.path.isdir(dir_b) else set()
    for f in sorted(files_a - files_b):
        fails.append(f"CROSS-COPY: {f} exists in {COPY_A}/ but is MISSING from {COPY_B}/")
    for f in sorted(files_b - files_a):
        fails.append(f"CROSS-COPY: {f} exists in {COPY_B}/ but is MISSING from {COPY_A}/")
    for f in sorted(files_a & files_b):
        ba = open(os.path.join(dir_a, f), "rb").read()
        bb = open(os.path.join(dir_b, f), "rb").read()
        if ba != bb:
            dl = _diff_line_count(ba.decode("utf-8", "replace"), bb.decode("utf-8", "replace"))
            fails.append(f"CROSS-COPY: {f} DIFFERS between {COPY_A}/ and {COPY_B}/ — "
                         f"{dl} line(s) differ")
    # Completeness: a file missing from BOTH copies passes the pairwise check above (same
    # on both sides) but is still a delta-audit gap — catch it here.
    if files_a == files_b:
        missing_known = KNOWN_FILES - files_a
        if missing_known:
            fails.append(f"CROSS-COPY: both copies are missing known file(s): "
                         f"{sorted(missing_known)}")
    return fails


# -------------------------------------------------------------------- arm 4: UNKNOWN FILES
def check_unknown_files(repo):
    fails = []
    for label, rel in (("machinery/", COPY_A), ("claude-plugin copy", COPY_B)):
        d = os.path.join(repo, rel)
        if not os.path.isdir(d):
            continue
        for f in sorted(_walk_files(d)):
            if f not in KNOWN_FILES:
                fails.append(f"UNKNOWN FILE: {rel}/{f} ({label}) is not on the known-files "
                             f"list {sorted(KNOWN_FILES)} — fail loud rather than silently "
                             f"ignored (scope-blindness rule)")
    return fails


# ------------------------------------------------------------------- arm 2: SHIM PROVENANCE
def check_shim_provenance(repo, git_root):
    fails = []
    shim_path = os.path.join(repo, COPY_A, SHIM_NAME)
    if not os.path.isfile(shim_path):
        fails.append(f"SHIM PROVENANCE: {COPY_A}/{SHIM_NAME} does not exist — cannot read "
                     f"its docstring")
        return fails
    shim_text = open(shim_path, encoding="utf-8").read()

    m_a = DOCSTRING_COMMIT_RE_A.search(shim_text)
    if not m_a:
        fails.append(
            f"SHIM PROVENANCE: could not find the '{SHIM_SOURCE_FILE_A} @ HEAD `<hash>`' "
            f"provenance line in {COPY_A}/{SHIM_NAME}'s docstring — the docstring format "
            f"changed; this gate reads that line and cannot check silently blind.")
    elif m_a.group(1) != PORT_COMMIT_A:
        fails.append(
            f"SHIM PROVENANCE: {COPY_A}/{SHIM_NAME}'s docstring now claims it was ported "
            f"from {SHIM_SOURCE_FILE_A} @ {m_a.group(1)}, but this gate is built against "
            f"{PORT_COMMIT_A} — the shim was re-ported and the gate was not updated to match.")

    m_b = DOCSTRING_COMMIT_RE_B.search(shim_text)
    if not m_b:
        fails.append(
            f"SHIM PROVENANCE: could not find the '{SHIM_SOURCE_FILE_B} @ HEAD `<hash>`' "
            f"dependency line in {COPY_A}/{SHIM_NAME}'s docstring — the docstring format "
            f"changed; this gate reads that line to know which commit to audit "
            f"GM_VOCAB/LS_VOCAB against.")
    elif m_b.group(1) != PORT_COMMIT_B:
        fails.append(
            f"SHIM PROVENANCE: {COPY_A}/{SHIM_NAME}'s docstring now claims GM_VOCAB/LS_VOCAB "
            f"were ported from {SHIM_SOURCE_FILE_B} @ {m_b.group(1)}, but this gate is built "
            f"against {PORT_COMMIT_B} — update PORT_COMMIT_B.")

    def _chain(cur_relpath, source_file, commit, names, chain_label):
        cur_path = os.path.join(repo, cur_relpath)
        if not os.path.isfile(cur_path):
            fails.append(f"SHIM PROVENANCE {chain_label}: {cur_relpath} does not exist — "
                         f"cannot audit")
            return
        cur_text = open(cur_path, encoding="utf-8").read()
        old_text, err = _git_show(git_root, commit, source_file)
        if err:
            fails.append(f"SHIM PROVENANCE {chain_label}: could not read {source_file} @ "
                         f"{commit} — {err}")
            return
        cur_seg = extract_named(cur_text, names)
        old_seg = extract_named(old_text, names)
        for n in names:
            o = old_seg.get(n)
            if o is None:
                fails.append(f"SHIM PROVENANCE {chain_label}: {n!r} not found in "
                             f"{source_file} @ {commit} itself — the shim's own claim "
                             f"cannot be verified against its declared source")
                continue
            c = cur_seg.get(n)
            if c is None:
                fails.append(f"SHIM PROVENANCE {chain_label}: {n!r} is GONE from current "
                             f"{cur_relpath} (present at the port commit {commit}) — the "
                             f"shim's ported source no longer exists to compare against")
                continue
            if c != o:
                dl = _diff_line_count(o, c)
                fails.append(f"SHIM PROVENANCE {chain_label}: {n!r} in {cur_relpath} has "
                             f"CHANGED since the port commit {commit} — {dl} line(s) differ. "
                             f"{COPY_A}/{SHIM_NAME} may now be stale against its declared "
                             f"source; re-review and re-port, or update the docstring.")

    _chain("knowledge/_capture_gate.py", SHIM_SOURCE_FILE_A, PORT_COMMIT_A,
           PORTED_FUNCS_A + PORTED_CONSTS_A, "chain(a)")
    _chain("knowledge/_gm_usage.py", SHIM_SOURCE_FILE_B, PORT_COMMIT_B,
           PORTED_CONSTS_B, "chain(b)")
    return fails


# --------------------------------------------------------------------------------- run
def run(repo=None, git_root=None):
    repo = ROOT if repo is None else repo
    git_root = ROOT if git_root is None else git_root
    fails = []
    fails += check_verbatim_set(repo)
    fails += check_cross_copy_identity(repo)
    fails += check_unknown_files(repo)
    fails += check_shim_provenance(repo, git_root)
    return fails


def main():
    fails = run()
    print(f"memento-package delta-audit: {len(fails)} failure(s)")
    for f in fails:
        print(f"  ✗ {f}")
    if not fails:
        print("  ✅ VERBATIM SET byte-identical (both copies) · shim provenance clean "
              "(both chains) · copies identical to each other · no unknown files")
        return 0
    print(f"\n❌ memento-package delta-audit FAILED — {len(fails)} finding(s) above. "
          f"See memento-package/_PACKAGE-SPEC.md:13-14 (Dave's #64 boundary ruling: "
          f"copies only, every copy delta-audited).")
    return 1


# --------------------------------------------------------------------------- selftest
def _make_fixture():
    """A /tmp copy of exactly the files this gate reads: the 5 knowledge/ sources and the
    whole memento-package/ subtree (__pycache__ excluded at copy time). Mutations in the
    selftest below land ONLY inside this directory — the real repo's files are never
    opened for writing anywhere in this module. `git_root` for provenance lookups stays
    pointed at the REAL repo (ROOT) even when `repo` points here, because `git show` reads
    the object database only — it touches no working-tree file and no index, so pointing
    it at ROOT during a mutation test does not run any mutation against the real repo."""
    d = tempfile.mkdtemp(prefix="pkgdelta_fixture_")
    os.makedirs(os.path.join(d, "knowledge"))
    for f in ("_gen_chain.py", "_memento_search.py", "_search_core.py", "_capture_gate.py",
              "_gm_usage.py"):
        shutil.copy(os.path.join(ROOT, "knowledge", f), os.path.join(d, "knowledge", f))
    shutil.copytree(os.path.join(ROOT, "memento-package"),
                     os.path.join(d, "memento-package"),
                     ignore=shutil.ignore_patterns("__pycache__"))
    return d


def _mutate_insert_marker(path, name):
    """Insert a comment-only line inside `name`'s (function or Assign) span in the file at
    `path` — always syntactically valid Python, changes the AST source-segment hash without
    needing to know the function's current body text."""
    text = open(path, encoding="utf-8").read()
    tree = ast.parse(text)
    node = _find_node(tree, name)
    assert node is not None, f"fixture setup: {name!r} not found in {path}"
    lines = text.splitlines(keepends=True)
    lines.insert(node.lineno, "    # MUTATION-TEST MARKER — do not ship\n")
    open(path, "w", encoding="utf-8").write("".join(lines))


def _mutate_delete_node(path, name):
    """Delete `name`'s (function or Assign) lines entirely from the file at `path`."""
    text = open(path, encoding="utf-8").read()
    tree = ast.parse(text)
    node = _find_node(tree, name)
    assert node is not None, f"fixture setup: {name!r} not found in {path}"
    lines = text.splitlines(keepends=True)
    del lines[node.lineno - 1: node.end_lineno]
    open(path, "w", encoding="utf-8").write("".join(lines))


def selftest():
    fails = []

    def bite(what, ok):
        print(f"    {'✓' if ok else '✗'} {what}")
        if not ok:
            fails.append(what)

    # ---- (0) POSITIVE — the real, now-repaired repo passes clean, all four arms.
    real_fails = run()
    bite(f"real repo: clean (0 findings; got {len(real_fails)}: {real_fails[:2]})",
         real_fails == [])

    # ---- ARM 1 — VERBATIM SET -----------------------------------------------------
    d = _make_fixture()
    try:
        target = os.path.join(d, COPY_A, "_gen_chain.py")
        with open(target, "a", encoding="utf-8") as f:
            f.write("\n# mutation: one extra line\n")
        found = check_verbatim_set(d)
        bite("ARM1 mutation: doctored machinery/_gen_chain.py is caught, names the file "
             "+ copy + a line count",
             any("_gen_chain.py" in x and "machinery/" in x and "line(s) differ" in x
                 for x in found))
        if found:
            print(f"      quoted: {found[0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    d = _make_fixture()
    try:
        os.remove(os.path.join(d, COPY_B, "_search_core.py"))
        found = check_verbatim_set(d)
        bite("ARM1 mutation: a MISSING verbatim file (not just a diff) is caught and named",
             any("_search_core.py" in x and "MISSING" in x for x in found))
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # ---- ARM 3 — CROSS-COPY IDENTITY ------------------------------------------------
    d = _make_fixture()
    try:
        target = os.path.join(d, COPY_B, "_MACHINERY-MANIFEST.md")
        with open(target, "a", encoding="utf-8") as f:
            f.write("\nmutation: copy B only\n")
        found = check_cross_copy_identity(d)
        bite("ARM3 mutation: copies diverge on a non-verbatim-set file (the manifest) — "
             "caught, names the file and 'DIFFERS between'",
             any("_MACHINERY-MANIFEST.md" in x and "DIFFERS between" in x for x in found))
        if found:
            print(f"      quoted: {found[0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    d = _make_fixture()
    try:
        os.remove(os.path.join(d, COPY_A, "_consult-lexicon.json"))
        os.remove(os.path.join(d, COPY_B, "_consult-lexicon.json"))
        found = check_cross_copy_identity(d)
        bite("ARM3 mutation: a known file missing from BOTH copies (pairwise-invisible) "
             "is still caught by the completeness sub-check",
             any("both copies are missing known file" in x and "_consult-lexicon.json" in x
                 for x in found))
        if found:
            print(f"      quoted: {found[0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # ---- ARM 4 — UNKNOWN FILES -------------------------------------------------------
    d = _make_fixture()
    try:
        rogue = os.path.join(d, COPY_A, "_ROGUE.py")
        open(rogue, "w", encoding="utf-8").write("# should never be here\n")
        pycache = os.path.join(d, COPY_A, "__pycache__")
        os.makedirs(pycache, exist_ok=True)
        open(os.path.join(pycache, "junk.pyc"), "wb").write(b"\x00\x01")
        found = check_unknown_files(d)
        bite("ARM4 mutation: a rogue file is caught, named with its exact path",
             any("_ROGUE.py" in x and "UNKNOWN FILE" in x for x in found))
        bite("ARM4 control: __pycache__ present in the SAME fixture is excluded BY NAME "
             "and never itself reported (proves the exclusion is narrow, not a silent "
             "blanket ignore)",
             not any("__pycache__" in x or "pycache" in x for x in found)
             and len(found) == 1)
        if found:
            print(f"      quoted: {found[0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # ---- ARM 2 — SHIM PROVENANCE ------------------------------------------------------
    # (a) a ported FUNCTION's body changes in knowledge/_capture_gate.py since the port.
    d = _make_fixture()
    try:
        _mutate_insert_marker(os.path.join(d, "knowledge", "_capture_gate.py"),
                              "measure_tokens")
        found = check_shim_provenance(d, ROOT)
        bite("ARM2(a) mutation: measure_tokens body changed since port commit 91d7528 — "
             "caught, names the function and 'CHANGED since the port'",
             any("measure_tokens" in x and "CHANGED since the port" in x for x in found))
        if found:
            print(f"      quoted: {[x for x in found if 'measure_tokens' in x][0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # (b) a ported function is deleted outright from knowledge/_capture_gate.py.
    d = _make_fixture()
    try:
        _mutate_delete_node(os.path.join(d, "knowledge", "_capture_gate.py"),
                            "measurement_degraded")
        found = check_shim_provenance(d, ROOT)
        bite("ARM2(b) mutation: measurement_degraded deleted from current source — "
             "caught, names the function and 'GONE from current'",
             any("measurement_degraded" in x and "GONE from current" in x for x in found))
        if found:
            print(f"      quoted: {[x for x in found if 'measurement_degraded' in x][0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # (c) a ported CONSTANT changes in knowledge/_gm_usage.py (chain b) since the port.
    d = _make_fixture()
    try:
        _mutate_insert_marker(os.path.join(d, "knowledge", "_gm_usage.py"), "GM_VOCAB")
        found = check_shim_provenance(d, ROOT)
        bite("ARM2(c) mutation: GM_VOCAB changed since port commit ace3ed3 — caught, "
             "names GM_VOCAB and 'CHANGED since the port'",
             any("GM_VOCAB" in x and "CHANGED since the port" in x for x in found))
        if found:
            print(f"      quoted: {[x for x in found if 'GM_VOCAB' in x][0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # (d) the shim's OWN docstring claims a different source commit than the gate expects.
    d = _make_fixture()
    try:
        shim_path = os.path.join(d, COPY_A, SHIM_NAME)
        text = open(shim_path, encoding="utf-8").read()
        # ⚠ #114: parametrised on PORT_COMMIT_A, never a hard-coded hash. The old literal
        # ("91d7528") rotted the moment the shim was legitimately re-ported, and it mutated
        # every OTHER mention of that hash in the docstring too — so the bite silently stopped
        # exercising the DECLARED-provenance line it exists to test.
        m = DOCSTRING_COMMIT_RE_A.search(text)
        assert m and m.group(1) == PORT_COMMIT_A
        text = text[:m.start(1)] + "deadbee" + text[m.end(1):]
        open(shim_path, "w", encoding="utf-8").write(text)
        found = check_shim_provenance(d, ROOT)
        bite("ARM2(d) mutation: shim docstring's claimed commit no longer matches the "
             "gate's expectation — caught, names both hashes",
             any("deadbee" in x and PORT_COMMIT_A in x for x in found))
        if found:
            print(f"      quoted: {[x for x in found if 'deadbee' in x][0]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    if fails:
        print(f"  ✗ _validate_package_delta selftest: {len(fails)} bite(s) failed")
        return 1
    print("  ✅ _validate_package_delta selftest: all bites pass")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
