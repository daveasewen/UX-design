#!/usr/bin/env python3
"""_gate_pack_imports.py — does every Python file in a baked pack actually IMPORT?

⬛ ADVISORY AT BIRTH (#220). This gate reports and does not block. Exit is 0 whatever it finds
unless you pass `--strict`, and nothing wires `--strict` today. **Promotion to blocking is Dave's
word**, exactly like `_gate_minted_consumption.py` — a gate that starts blocking is a gate that
can stop a release, and that is a decision, not an implementation detail.

WHY IT EXISTS — the defect it was built from, in one line.
`Apollo-Spider-v1.0.0.zip` shipped `memento-package/claude-plugin/memento/machinery/_gen_chain.py`
and it cannot be imported: `ModuleNotFoundError: No module named '_could_not_ask'`. That file is
the chain generator — the first thing a Memento — Gumdrop designer touches on day one. The
package delta gate was GREEN over it. It had to be: it compares a VERBATIM SET of paths and
their bytes, and asks the two copies whether they are identical to each other. Both copies were
identical, and both were broken. **Nothing in the release chain ever ran a single packed file.**
[[no-gate-parses-the-artefact]] — the first gate over an artefact must read it in the CONSUMER's
grammar, and Python's grammar for a module is `import`, not `sha256`.

HOW IT ASKS. Not statically. `sys.path` is decided at runtime by the file itself — these modules
insert their own directory, walk upward looking for `_helpgate.py`, and join paths out of
`__file__` — so any static model of resolution is a guess that can be confidently wrong. This
gate copies the pack into a THROWAWAY directory and imports each `.py` there, in its own
subprocess, with its own directory on `sys.path`, under `__name__ = "_packprobe_<n>"` so that
`if __name__ == "__main__"` blocks and help gates do not fire. The copy is why importing is safe:
a module whose top level writes a file writes it into the throwaway, and the throwaway is
deleted. Nothing is imported into THIS process.

WHAT COUNTS AS A FAILURE, and what deliberately does not.
  · MISSING-LOCAL — the module it wants is carried by the pack SOMEWHERE but is not reachable
    from where the importer landed. **This is the defect class.** It is a packaging decision that
    went wrong, and it is always the pack's fault.
  · MISSING-THIRD-PARTY — `playwright`, `PIL`. A named `pip install` is a documented
    prerequisite, not a packaging fence: `_gen_pack_manifest.py` already ships those gates under
    the NEEDS-DEP verdict on Dave's own page. Reported, never counted as a red.
  · ERROR-AT-IMPORT — the file imported its dependencies and then raised doing something else at
    module level. Named separately, because the cure is different.
  · RAN-AS-SCRIPT — a `SystemExit` at module level. Several validators in this repo do their
    whole job at module scope and end in `sys.exit(1 if fails else 0)`, so importing them RUNS
    them. Exit 0 is a clean run and is NOT a finding; a non-zero exit is the gate's own verdict
    about the pack's contents and belongs to that gate, not to this one — it is named and
    excluded from this gate's reds, because reporting another gate's honest red as a packaging
    defect is how a new instrument earns a reputation for crying wolf.
  · NEEDS-ARGV — an `IndexError` whose own traceback indexes `sys.argv`: a CLI tool that does
    its job at module scope, asked for nothing and saying so. `_embed_kg_fragment.py` is one, and
    it was written up as a broken packed builder TWICE before this bucket existed. The predicate
    keys on the traceback, never on the exception type, so an ordinary `IndexError` stays a red.
  · TIMEOUT — a module that does real work at import. Named, never silently dropped.

⛔ EVERY REFUSAL NAMES THE MODULE AND THE FILE. A gate that says "3 files failed" cannot be acted
on, and a gate that passes quietly when it could not look is worse than no gate at all
[[a-crash-is-not-a-fail]] [[instrument-without-a-consumer]]. If the pack holds no `.py` at all,
this gate says so and refuses to call that green.

⛔ ONE PROBE MUST NOT POISON THE NEXT — and in this gate's FIRST live run it did (#220 addendum).
The throwaway copy protects the SUBJECT from the gate. It does not protect the probes from EACH
OTHER, and the first version of this gate shared one copy across all 76 imports. Measured
consequence, on the v1.0.1 stage and on the shipped v1.0.0 zip alike:

    knowledge/compliance/_build_compliance_kg.py   does its whole job at module level and
        REWRITES knowledge/compliance/graph-index.json, dropping the `verification` and
        `external_automatable_refs` blocks that `_build_verification_edges.py` adds later in
        `_build_all.py`'s ordered serial (step 1 writes it, step 8 completes it).
    knowledge/compliance/_build_kg_diagram.py      imported AFTER it, read the half-written
    knowledge/compliance/_embed_kg_fragment.py     index and died: KeyError: 'verification'.

Both were reported as ERROR-AT-IMPORT and written up as two pre-existing packaging defects. They
are not defects. On a PRISTINE copy `_build_kg_diagram.py` imports and runs clean
(`nsc 38 · ncomp 133 · nedge 816 · verified 4 · axe 16`) and `_embed_kg_fragment.py` asks for the
argv it needs (`IndexError` at `trace = sys.argv[1]`). The gate manufactured its own red, and an
instrument that reports its own side effect as the subject's defect is measuring itself
[[green-tests-cannot-see-scope]] [[mutation-tests-the-clause-not-the-feature]].

So: a PRISTINE TREE PER PROBE. A template copy is held aside, the tree is snapshotted before and
after every import, and anything a module touched is put back before the next one runs. What the
module wrote is not discarded — it is REPORTED as WRITES-AT-IMPORT with the paths named, because
"this file rewrites shipped data just by being imported" is a true and useful thing to know about
a pack, and it is the fact that would have prevented the false finding in the first place.

Usage:
    python3 knowledge/_gate_pack_imports.py --zip apollo-spider/dist/Apollo-Spider-v1.0.0.zip
    python3 knowledge/_gate_pack_imports.py --stage /var/tmp/spider-stage
    python3 knowledge/_gate_pack_imports.py --zip <z> --strict     # exit 1 on a red (NOT WIRED)
    python3 knowledge/_gate_pack_imports.py --selftest

THE KNOWN-ANSWER TEST (#220, and it is the reason to believe this gate at all). Run it against
`apollo-spider/dist/Apollo-Spider-v1.0.0.zip`. It must report exactly one MISSING-LOCAL:
`memento-package/claude-plugin/memento/machinery/_gen_chain.py` wanting `_could_not_ask`. A gate
that is green on the pack we KNOW is broken is measuring nothing.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

PER_FILE_TIMEOUT = 25

# The driver. It runs in a subprocess, in the throwaway copy, and prints ONE json line.
# `__name__` is deliberately not "__main__": a packed gate's main() must not run, and the
# repo-wide help-gate preamble is a no-op for any other name.
DRIVER = r'''
import importlib.util, json, os, sys, traceback
target = os.environ["PACKPROBE_TARGET"]
# ⛔ THE GATE'S OWN ARGV MUST NOT LEAK INTO THE SUBJECT (#220 addendum). The target used to be
# passed as sys.argv[1]. Packed modules that do their work at module level READ sys.argv[1] —
# and `knowledge/compliance/_build_kg_diagram.py` took it as its OUTPUT path and overwrote
# itself with 56,547 bytes of HTML (measured, in the throwaway). The probe's argument became
# the subject's argument. It is passed in the environment now, and the module is shown the
# argv an unargumented run would give it: argv[0] only. A module that needs an argument then
# says so honestly (IndexError) instead of being handed the gate's private path.
sys.argv = [target]
sys.path.insert(0, os.path.dirname(os.path.abspath(target)))
name = "_packprobe_" + os.path.basename(target)[:-3].replace("-", "_").replace(".", "_")
out = {"ok": True}
try:
    spec = importlib.util.spec_from_file_location(name, target)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
except SystemExit as e:
    out = {"ok": False, "type": "SystemExit", "msg": "exit %r" % (e.code,),
           "code": (0 if e.code is None else e.code), "missing": "", "tb": ""}
except BaseException as e:
    out = {"ok": False, "type": type(e).__name__, "msg": str(e)[:400],
           "missing": getattr(e, "name", None) or "",
           "tb": traceback.format_exc()[-600:]}
sys.stdout.write("\x01PACKPROBE\x01" + json.dumps(out))
'''

MOD_RE = re.compile(r"No module named ['\"]([A-Za-z0-9_.]+)['\"]")


def py_files(root):
    out = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for f in files:
            if f.endswith(".py"):
                out.append(os.path.relpath(os.path.join(d, f), root))
    return sorted(out)


def carried_modules(root):
    """Every module name the pack carries a file for, anywhere. The bridge between
    'missing because we packed it badly' and 'missing because it is somebody else's library'."""
    return {os.path.basename(p)[:-3] for p in py_files(root)}


DRIVER_NAME = "_packprobe_driver.py"


def tree_state(root):
    """(size, mtime_ns) per path — enough to SEE a write, cheap enough to run per probe.

    Not a hash: 1,641 files x 76 probes is 125k stats (fast) or 125k file reads (not). A
    module that rewrites a file byte-identically is invisible here, and that is declared,
    not hidden — an invisible write is also a write that changed nothing for the next probe,
    which is the only thing this snapshot exists to prevent."""
    out = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for f in files:
            if f == DRIVER_NAME and d == root:
                continue          # the gate's own probe is not part of the subject
            p = os.path.join(d, f)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            out[os.path.relpath(p, root)] = (st.st_size, st.st_mtime_ns)
    return out


def _put_back(rel, root, template):
    """Restore ONE path in root from the pristine template (or delete what template lacks)."""
    dst, src = os.path.join(root, rel), os.path.join(template, rel)
    if os.path.lexists(dst):
        if os.path.islink(dst) or os.path.isfile(dst):
            os.remove(dst)
        else:
            shutil.rmtree(dst, ignore_errors=True)
    if not os.path.lexists(src):
        return                                  # the module ADDED it; the pack does not carry it
    os.makedirs(os.path.dirname(dst) or root, exist_ok=True)
    if os.path.islink(src):
        os.symlink(os.readlink(src), dst)
    else:
        shutil.copy2(src, dst)


def restore(root, template, base, now):
    """Put every path a probe touched back. Returns the sorted list of touched paths."""
    touched = sorted(set(base) ^ set(now) | {p for p in (set(base) & set(now))
                                             if base[p] != now[p]})
    for rel in touched:
        _put_back(rel, root, template)
    return touched


def probe(root, verbose=False):
    """Import every .py under root, in root, EACH ONE against a pristine tree.

    Returns a list of result dicts; a dict may carry `wrote` — the paths that import touched."""
    files = py_files(root)
    carried = carried_modules(root)
    template = tempfile.mkdtemp(prefix="packimports-pristine-", dir="/var/tmp")
    tpl = os.path.join(template, "t")
    shutil.copytree(root, tpl, symlinks=True)
    base = tree_state(root)
    drv = os.path.join(root, DRIVER_NAME)
    open(drv, "w").write(DRIVER)
    results = []
    try:
        for rel in files:
            if rel == DRIVER_NAME:
                continue
            full = os.path.join(root, rel)
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PACKPROBE_TARGET"] = full      # NOT argv — see the DRIVER's own comment
            try:
                r = subprocess.run([sys.executable, drv], cwd=root, env=env,
                                   capture_output=True, timeout=PER_FILE_TIMEOUT)
                raw = r.stdout.decode("utf8", "replace")
                marker = raw.rsplit("\x01PACKPROBE\x01", 1)
                if len(marker) != 2:
                    res = dict(file=rel, verdict="ERROR-AT-IMPORT", module="",
                               why="the probe produced no verdict line: " +
                                   (r.stderr.decode("utf8", "replace")[-200:] or "no stderr"))
                else:
                    d = json.loads(marker[1])
                    if d["ok"]:
                        res = dict(file=rel, verdict="OK", module="", why="")
                    else:
                        miss = d.get("missing") or ""
                        m = MOD_RE.search(d.get("msg", "") or "")
                        if not miss and m:
                            miss = m.group(1)
                        top = miss.split(".")[0]
                        if d["type"] == "SystemExit":
                            verdict = "RAN-AS-SCRIPT"
                        elif d["type"] in ("ModuleNotFoundError", "ImportError") and top:
                            verdict = ("MISSING-LOCAL" if top in carried
                                       else "MISSING-THIRD-PARTY")
                        elif d["type"] == "IndexError" and "sys.argv" in (d.get("tb") or ""):
                            # NEEDS-ARGV, and the predicate is deliberately narrow: an IndexError
                            # whose own traceback line indexes sys.argv. `_embed_kg_fragment.py`
                            # is a CLI tool that does its job at module scope — handed no
                            # argument it says so, and that is the tool working, not the pack
                            # broken. Calling it a packaging red is the crying-wolf failure the
                            # RAN-AS-SCRIPT bucket already exists to prevent.
                            verdict = "NEEDS-ARGV"
                        else:
                            verdict = "ERROR-AT-IMPORT"
                        res = dict(file=rel, verdict=verdict, module=top,
                                   code=d.get("code", 0), tb=d.get("tb", ""),
                                   why="%s: %s" % (d["type"], d["msg"]))
            except subprocess.TimeoutExpired:
                res = dict(file=rel, verdict="TIMEOUT", module="",
                           why="did not finish importing in %ds" % PER_FILE_TIMEOUT)
            # PRISTINE TREE PER PROBE. Whatever this import wrote is named and then undone, so
            # the NEXT file is measured against the pack as baked and never against the residue
            # of the file before it. This is the #220-addendum fix; see the docstring.
            touched = restore(root, tpl, base, tree_state(root))
            if touched:
                res["wrote"] = touched
            results.append(res)
            if verbose and (res["verdict"] != "OK" or touched):
                print("  %-18s %s%s" % (res["verdict"], rel,
                                        "  (wrote %d path(s))" % len(touched) if touched else ""),
                      flush=True)
    finally:
        if os.path.exists(drv):
            os.remove(drv)
        shutil.rmtree(template, ignore_errors=True)
    return results


def pack_root_of(d):
    """A baked pack unzips to ONE root directory. A stage IS the root."""
    entries = [e for e in os.listdir(d) if not e.startswith(".")]
    if len(entries) == 1 and os.path.isdir(os.path.join(d, entries[0])):
        return os.path.join(d, entries[0])
    return d


def report(results, label):
    """Prints the reading. Returns (n_local, n_other) — reds and named non-reds."""
    buckets = {}
    for r in results:
        buckets.setdefault(r["verdict"], []).append(r)
    n = len(results)
    print("⬛ PACK IMPORT GATE (ADVISORY) — %s" % label)
    if n == 0:
        print("  ⛔ REFUSED: the pack holds NO .py files. This gate has nothing to import, and "
              "an instrument with no subject must not report green "
              "[[instrument-without-a-consumer]].")
        return -1, 0
    print("  %d python file(s) imported in an isolated copy · %s"
          % (n, " · ".join("%s %d" % (k, len(v)) for k, v in sorted(buckets.items()))))
    local = buckets.get("MISSING-LOCAL", [])
    for r in local:
        print("  ⛔ MISSING-LOCAL  %s" % r["file"])
        print("       wants `%s`, which this pack CARRIES but not where this file can reach it."
              % r["module"])
        print("       %s" % r["why"])
    for r in buckets.get("ERROR-AT-IMPORT", []) + buckets.get("TIMEOUT", []):
        print("  ⚠ %-16s %s" % (r["verdict"], r["file"]))
        print("       %s" % r["why"])
    scripts = buckets.get("RAN-AS-SCRIPT", [])
    if scripts:
        clean = [r for r in scripts if not r.get("code")]
        noisy = [r for r in scripts if r.get("code")]
        print("  ⬛ RAN-AS-SCRIPT — %d file(s) do their whole job at module level, so importing "
              "them ran them: %d exited 0 (clean)." % (len(scripts), len(clean)))
        for r in noisy:
            print("       ⚠ %s ended %s — that is THAT gate's verdict about the pack, not a "
                  "packaging defect. Read it there." % (r["file"], r["why"]))
    argvs = buckets.get("NEEDS-ARGV", [])
    if argvs:
        print("  ⬛ NEEDS-ARGV — %d file(s) are CLI tools that do their work at module scope. "
              "Given no argument they say so. Not a packaging defect; named so it is never "
              "re-triaged as one." % len(argvs))
        for r in argvs:
            print("       %s — %s" % (r["file"], r["why"]))
    writers = [r for r in results if r.get("wrote")]
    if writers:
        print("  ⬛ WRITES-AT-IMPORT — %d file(s) changed the pack just by being imported. Each "
              "was put back before the next probe ran, so no verdict below it is contaminated."
              % len(writers))
        for r in writers:
            shown = r["wrote"][:4]
            print("       %s -> %s%s" % (r["file"], ", ".join(shown),
                                         " (+%d more)" % (len(r["wrote"]) - len(shown))
                                         if len(r["wrote"]) > len(shown) else ""))
    tp = sorted({r["module"] for r in buckets.get("MISSING-THIRD-PARTY", [])})
    if tp:
        print("  ⬛ DECLARED, NOT FAILED — %d file(s) want third-party module(s) the pack does "
              "not and should not carry: %s" % (len(buckets["MISSING-THIRD-PARTY"]), ", ".join(tp)))
    other = len(buckets.get("ERROR-AT-IMPORT", [])) + len(buckets.get("TIMEOUT", []))
    if not local and not other:
        print("  ✅ every packed module imports from where it lands.")
    print("  ⬛ ADVISORY — this gate does not block. Promotion is Dave's word.")
    return len(local), other


def run(target, is_zip, strict=False, verbose=False, keep=None):
    tmp = keep or tempfile.mkdtemp(prefix="packimports-", dir="/var/tmp")
    try:
        if is_zip:
            with zipfile.ZipFile(target) as z:
                z.extractall(tmp)
            root = pack_root_of(tmp)
        else:
            # COPY, never probe in place: importing runs module-level code, and a module that
            # writes must write into the throwaway. A gate that mutates its own subject is not
            # a measurement.
            root = os.path.join(tmp, "stage")
            shutil.copytree(target, root, symlinks=True)
            root = pack_root_of(root) if len(os.listdir(root)) == 1 else root
        results = probe(root, verbose=verbose)
        local, other = report(results, target)
        if local < 0:
            return 1 if strict else 0
        return 1 if (strict and (local or other)) else 0
    finally:
        if keep is None:
            shutil.rmtree(tmp, ignore_errors=True)


# -------------------------------------------------------------------------------------------
# selftest — the classifier is bitten in BOTH directions on a synthetic pack, because a gate
# that has only ever seen a green pack has never been shown to bite.
# -------------------------------------------------------------------------------------------

def selftest():
    fails, n = [], [0]

    def bite(name, got, want, why=""):
        n[0] += 1
        if got != want:
            fails.append("[%s] got %r, wanted %r %s" % (name, got, want, why))

    tmp = tempfile.mkdtemp(prefix="packimports-st-", dir="/var/tmp")
    try:
        # A pack in the v1.0.0 SHAPE: two mirrored machinery dirs, the sibling in only one.
        for d in ("memento-package/machinery",
                  "memento-package/claude-plugin/memento/machinery", "knowledge"):
            os.makedirs(os.path.join(tmp, d))
        body = ("import os, sys\n"
                "HERE = os.path.dirname(os.path.abspath(__file__))\n"
                "sys.path.insert(0, HERE)\n"
                "import _could_not_ask\n")
        open(os.path.join(tmp, "memento-package/machinery/_could_not_ask.py"), "w").write("X=1\n")
        open(os.path.join(tmp, "memento-package/machinery/_gen_chain.py"), "w").write(body)
        open(os.path.join(tmp,
             "memento-package/claude-plugin/memento/machinery/_gen_chain.py"), "w").write(body)
        open(os.path.join(tmp, "knowledge/_needs_dep.py"), "w").write(
            "import a_module_that_is_definitely_not_installed_xyz\n")
        open(os.path.join(tmp, "knowledge/_boom.py"), "w").write("raise ValueError('boom')\n")
        open(os.path.join(tmp, "knowledge/_script_clean.py"), "w").write(
            "import sys\nsys.exit(0)\n")
        open(os.path.join(tmp, "knowledge/_script_red.py"), "w").write(
            "import sys\nsys.exit(1)\n")
        # THE #220-ADDENDUM SHAPE, reproduced synthetically: an alphabetically EARLIER module
        # rewrites a shipped data file at import and drops a key a LATER module reads. Before
        # the pristine-tree-per-probe fix this pair reported the reader as a packaging defect.
        # `_aaa_` and `_zzz_` pin the probe order, because the defect IS an ordering defect.
        open(os.path.join(tmp, "knowledge/shared.json"), "w").write(
            '{"totals": 1, "verification": {"ok": true}}\n')
        open(os.path.join(tmp, "knowledge/_aaa_writer.py"), "w").write(
            "import json, os\n"
            "P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared.json')\n"
            "json.dump({'totals': 1}, open(P, 'w'))\n")     # drops `verification`, as step 1 does
        open(os.path.join(tmp, "knowledge/_zzz_reader.py"), "w").write(
            "import json, os\n"
            "P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared.json')\n"
            "V = json.load(open(P))['verification']\n")
        # THE ARGV LEAK, bitten in the shape that caused it: a module that treats sys.argv[1] as
        # an output path. Handed the gate's own argument it overwrote ITSELF (measured on
        # `_build_kg_diagram.py`: 13,027 bytes of Python became 56,547 bytes of HTML). Shown an
        # unargumented argv it must say what it needs instead.
        open(os.path.join(tmp, "knowledge/_argv_writer.py"), "w").write(
            "import sys\n"
            "open(sys.argv[1], 'w').write('CLOBBERED')\n")
        open(os.path.join(tmp, "knowledge/_bad_index.py"), "w").write("X = [][3]\n")
        before_run = tree_state(tmp)
        res = {r["file"]: r for r in probe(tmp)}
        bite("gate/probe-argv-does-not-reach-the-module",
             (res["knowledge/_argv_writer.py"]["verdict"],
              res["knowledge/_argv_writer.py"].get("wrote")),
             ("NEEDS-ARGV", None),
             "the gate's private path became the subject's output path and destroyed a packed "
             "source file in the throwaway; `wrote` must be None — nothing was clobbered")
        bite("gate/argv-hungry-module-says-what-it-needs",
             "IndexError" in res["knowledge/_argv_writer.py"]["why"], True,
             "an honest 'I need an argument' beats a silent write to the gate's own path")
        bite("gate/needs-argv-is-not-a-packaging-red",
             res["knowledge/_argv_writer.py"]["verdict"], "NEEDS-ARGV",
             "a CLI tool asked for nothing is working; #220's `_embed_kg_fragment.py` was "
             "triaged twice as a defect because this bucket did not exist")
        # the narrow predicate, in the OTHER direction: an IndexError that is NOT about argv is
        # a real error and must stay one, or the bucket becomes a place reds go to hide.
        bite("gate/an-ordinary-IndexError-is-still-an-error",
             res["knowledge/_bad_index.py"]["verdict"], "ERROR-AT-IMPORT",
             "NEEDS-ARGV keys on sys.argv in the traceback, not on the exception TYPE")
        bite("gate/a-writer-does-not-poison-a-later-reader",
             res["knowledge/_zzz_reader.py"]["verdict"], "OK",
             "the #220 KeyError: 'verification' reds were THIS, and they were the gate's own "
             "side effect reported as the pack's defect")
        bite("gate/the-write-itself-is-reported",
             res["knowledge/_aaa_writer.py"].get("wrote"), ["knowledge/shared.json"],
             "undoing a write silently would hide the one fact that explains the class")
        bite("gate/subject-is-unchanged-after-the-run", tree_state(tmp), before_run,
             "a gate that leaves its subject mutated has measured something that no longer exists")
        bite("gate/sees-the-broken-copy",
             res["memento-package/claude-plugin/memento/machinery/_gen_chain.py"]["verdict"],
             "MISSING-LOCAL",
             "the whole reason this gate exists")
        bite("gate/names-the-module",
             res["memento-package/claude-plugin/memento/machinery/_gen_chain.py"]["module"],
             "_could_not_ask", "a refusal that does not name the module cannot be acted on")
        bite("gate/green-copy-is-green",
             res["memento-package/machinery/_gen_chain.py"]["verdict"], "OK",
             "the sibling copy resolves and must NOT be reported")
        bite("gate/third-party-is-not-a-packaging-red",
             res["knowledge/_needs_dep.py"]["verdict"], "MISSING-THIRD-PARTY",
             "a named pip install is a prerequisite, not a fence")
        bite("gate/non-import-error-is-its-own-bucket",
             res["knowledge/_boom.py"]["verdict"], "ERROR-AT-IMPORT")
        # a module-level sys.exit is a SCRIPT that ran, not a broken import. Both directions.
        bite("gate/clean-script-exit-is-not-a-red",
             (res["knowledge/_script_clean.py"]["verdict"],
              res["knowledge/_script_clean.py"]["code"]), ("RAN-AS-SCRIPT", 0))
        bite("gate/script-red-is-named-not-counted",
             (res["knowledge/_script_red.py"]["verdict"],
              res["knowledge/_script_red.py"]["code"]), ("RAN-AS-SCRIPT", 1),
             "another gate's honest red is not this gate's packaging defect")
        bite("gate/no-leftover-driver",
             os.path.exists(os.path.join(tmp, "_packprobe_driver.py")), False,
             "the gate must not leave its own probe behind in the subject")
        # the empty-subject refusal: a gate with nothing to look at must not report green
        empty = tempfile.mkdtemp(prefix="packimports-empty-", dir="/var/tmp")
        try:
            bite("gate/empty-pack-refuses", report(probe(empty), "empty")[0], -1,
                 "no .py to import is a REFUSAL, never a pass")
        finally:
            shutil.rmtree(empty, ignore_errors=True)
        # advisory by construction: a red exits 0 unless --strict is asked for
        z = os.path.join(tmp, "fixture.zip")
        with zipfile.ZipFile(z, "w") as zf:
            for rel in py_files(tmp):
                zf.write(os.path.join(tmp, rel), "P/" + rel)
        bite("gate/advisory-exit-is-zero", run(z, True, strict=False), 0,
             "ADVISORY AT BIRTH — promotion is Dave's word")
        bite("gate/strict-arm-can-fail", run(z, True, strict=True), 1,
             "the strict arm must be able to go red or the promotion would be a no-op")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("selftest: %d bites, %d fail(s)" % (n[0], len(fails)))
    for f in fails:
        print("  RED " + f)
    return not fails


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--zip")
    ap.add_argument("--stage")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()
    if a.help or not (a.zip or a.stage or a.selftest):
        print(__doc__)
        sys.exit(0)
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    target = a.zip or a.stage
    if not os.path.exists(target):
        print("REFUSED: %r does not exist" % target, file=sys.stderr)
        sys.exit(2)
    sys.exit(run(target, bool(a.zip), strict=a.strict, verbose=a.verbose))


if __name__ == "__main__":
    main()
