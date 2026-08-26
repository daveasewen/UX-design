#!/usr/bin/env python3
"""_gate_ci_template.py — the workflow the PACK ships must parse, and must not lie.

★ WHY. `s219-D4(3)` is "CI both halves": this repo's own gates, and a workflow template the pack
hands a designer for their project. The second half has a failure mode the first half does not —
it is never run here. A broken `on:` block, a step that calls a script the zip does not carry, a
`continue-on-error` quietly added to a step: none of that shows up in this repo's CI, and the
first person to find out is a designer whose workflow either does not start or reports success
while a check is red. So the template gets a gate on THIS side of the fence.

WHAT IT ASKS, in the consumer's own grammar (YAML, parsed — never a regex over the text, which
is the [[no-gate-parses-the-artefact]] rule the house learned at ds-039):

  1. STRUCTURE. The template parses; there is an `on:` trigger and at least one job; every job
     names `runs-on` and has steps; every step is either a `uses:` or a `run:`.
  2. NO SILENT SUPPRESSION. Not one `continue-on-error` anywhere in the template. The pack's
     README tells a designer that the honest way to switch a check off is to DELETE THE STEP,
     and a template that shipped a suppression of its own would teach the opposite in the only
     place anyone looks — the file itself.
  3. EVERY REFERENCED SCRIPT SHIPS. A `run:` that invokes something under `ci-template/` must
     name a file that exists, and — once that file is tracked at the commit the manifest was
     generated from — a file that is IN THE SHIP LIST. ⚠ Before it is tracked there, this arm
     DECLARES rather than fails: the ship list is a function of a commit, and a file that does
     not exist at that commit is honestly absent from it, not missing from it.
  4. THE README KEEPS ITS PROMISES. It must actually document the three verdicts and the
     delete-the-step rule; those two sentences are the reason the template is safe to hand over.
  5. THE RUNNER COMPILES, and knows the refusal code. A runner that treated 77 as a failure
     would turn every refusal into a red and the convention would be decoration.

If `actionlint` is on PATH it is run as well — a real linter beats a structural reading — but
its absence is not a hole, because arms 1-5 do not need it.

COULD-NOT-ASK (77): PyYAML is how this gate parses in the consumer's grammar. Where it is not
importable the gate REFUSES rather than fall back to reading YAML with string matching, which
would be a different, weaker question wearing this gate's name. In `.github/workflows/gates.yml`
the release job installs it; in the `gates` job the survey will see the refusal, print it in
full, and not count it — the same shape as [71], whose proof of record lives in another job.

Usage:
    python3 knowledge/_release/_gate_ci_template.py --check
    python3 knowledge/_release/_gate_ci_template.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse, ast, json, os, shutil, subprocess, sys, tempfile

import _could_not_ask as cna

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TEMPLATE_DIR = os.path.join(ROOT, "designer-skills-v3", "ci-template")
TEMPLATE_REL = "designer-skills-v3/ci-template"
WORKFLOW = "gates.yml"
RUNNER = "run-gates.py"
READMES = "README.md"

# The two promises the README makes to a designer. Both are checked as NEEDLES because both are
# load-bearing: the first is why a refusal is safe, the second is why an exception is honest.
README_NEEDLES = [
    ("COULD-NOT-ASK", "the three-verdict convention must be explained, or a 77 reads as a crash"),
    ("Delete the step", "the honest way to switch a check off must be spelled out"),
    ("continue-on-error", "the dishonest way must be named as the thing not to do"),
]


def _yaml():
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def _walk(node, key):
    """Every value stored under `key`, anywhere in the parsed document."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key:
                yield v
            yield from _walk(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v, key)


def _referenced_scripts(doc):
    """Paths under ci-template/ that a `run:` invokes, normalised to repo-relative."""
    out = []
    for run in _walk(doc, "run"):
        for token in str(run).replace("\n", " ").split():
            if "ci-template/" in token:
                out.append(TEMPLATE_REL + "/" + token.split("ci-template/", 1)[1])
    return sorted(set(out))


def _ship_list():
    """(paths, manifest_commit) from the generated manifest, or (None, None)."""
    p = os.path.join(HERE, "_v3_manifest.json")
    if not os.path.exists(p):
        return None, None
    man = json.load(open(p, encoding="utf-8"))
    return {q for g in man["groups"] for q in g["paths"]}, man.get("commit", "")


def _tracked_at(commit, path):
    if not commit:
        return False
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit, "--", path],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0 and bool(r.stdout.strip())


def check(tdir=None, quiet=False):
    tdir = tdir or TEMPLATE_DIR
    def say(*a):
        if not quiet:
            print(*a)

    wf = os.path.join(tdir, WORKFLOW)
    if not os.path.exists(wf):
        if quiet:
            return cna.EXIT
        return cna.refuse(TEMPLATE_REL + "/" + WORKFLOW,
                          "the pack-side workflow template is not on disk, so there is nothing "
                          "to validate")
    yaml = _yaml()
    if yaml is None:
        return cna.refuse(TEMPLATE_REL + "/" + WORKFLOW,
                          "PyYAML is not importable in this environment, and this gate parses "
                          "the template in YAML rather than guessing at it with string "
                          "matching. Install it (pip install pyyaml) — the release job in "
                          ".github/workflows/gates.yml does exactly that")

    text = open(wf, encoding="utf-8").read()
    fails = []
    notes = []

    # ---- 1. structure
    try:
        doc = yaml.safe_load(text)
    except Exception as e:                                   # noqa: BLE001 — any parse error
        say("❌ %s does not parse as YAML: %s: %s" % (WORKFLOW, e.__class__.__name__,
                                                      str(e).splitlines()[0][:160]))
        return 1
    if not isinstance(doc, dict):
        fails.append("%s does not parse to a mapping — a workflow must be a mapping" % WORKFLOW)
        doc = {}
    # PyYAML reads a bare `on:` key as the boolean True (the Norway problem). Either spelling is
    # the trigger block, and a gate that missed that would be wrong about a correct file.
    if "on" not in doc and True not in doc:
        fails.append("no `on:` trigger — a workflow with no trigger never runs")
    jobs = doc.get("jobs") or {}
    if not jobs:
        fails.append("no `jobs:` — nothing would run")
    for name, job in (jobs.items() if isinstance(jobs, dict) else []):
        if not isinstance(job, dict):
            fails.append("job %r is not a mapping" % name)
            continue
        if not job.get("runs-on"):
            fails.append("job %r names no `runs-on`" % name)
        steps = job.get("steps") or []
        if not steps:
            fails.append("job %r has no steps" % name)
        for i, st in enumerate(steps):
            if not isinstance(st, dict) or not (st.get("uses") or st.get("run")):
                fails.append("job %r step %d is neither a `uses:` nor a `run:`" % (name, i))

    # ---- 2. no silent suppression
    silenced = [v for v in _walk(doc, "continue-on-error")]
    if silenced:
        fails.append("%d step(s) carry `continue-on-error` — the pack's README tells a designer "
                     "to DELETE a step rather than silence it, and a template that ships a "
                     "suppression teaches the opposite in the only file anyone reads"
                     % len(silenced))

    # ---- 3. every referenced script ships
    ship, man_commit = _ship_list()
    for rel in _referenced_scripts(doc):
        local = os.path.join(ROOT, rel)
        if not os.path.exists(local):
            fails.append("the workflow runs %s, which does not exist" % rel)
            continue
        if ship is None:
            notes.append("no manifest on disk — %s could not be checked against a ship list" % rel)
        elif rel in ship:
            pass
        elif not _tracked_at(man_commit, rel):
            notes.append("%s is not in the ship list because it is not tracked at %s, the commit "
                         "the manifest names. It enters the list at the commit that lands it."
                         % (rel, (man_commit or "?")[:12]))
        else:
            fails.append("the workflow runs %s, which is TRACKED at the manifest's commit %s but "
                         "is NOT in the ship list — a designer would get a workflow calling a "
                         "file the zip does not contain" % (rel, man_commit[:12]))

    # ---- 4. the README keeps its promises
    rd = os.path.join(tdir, READMES)
    if not os.path.exists(rd):
        fails.append("no README beside the template — a workflow with no explanation is a file "
                     "nobody can safely change")
    else:
        rtext = open(rd, encoding="utf-8").read()
        for needle, why in README_NEEDLES:
            if needle.lower() not in rtext.lower():
                fails.append("the README never mentions %r — %s" % (needle, why))

    # ---- 5. the runner compiles and knows the refusal code
    rn = os.path.join(tdir, RUNNER)
    if not os.path.exists(rn):
        fails.append("no %s beside the template, but the workflow calls it" % RUNNER)
    else:
        src = open(rn, encoding="utf-8").read()
        try:
            ast.parse(src)
        except SyntaxError as e:
            fails.append("%s does not compile: line %s, %s" % (RUNNER, e.lineno, e.msg))
        if "77" not in src:
            fails.append("%s never mentions exit code 77 — a runner that cannot recognise a "
                         "COULD-NOT-ASK turns every refusal into a red" % RUNNER)

    # ---- the optional real linter
    linter = shutil.which("actionlint")
    if linter:
        r = subprocess.run([linter, wf], capture_output=True, text=True)
        if r.returncode != 0:
            fails.append("actionlint: " + (r.stdout + r.stderr).strip().splitlines()[0][:200])
        else:
            notes.append("actionlint: clean")
    else:
        notes.append("actionlint is not installed — the structural arms above carry the check")

    say("ci-template gate — %s" % os.path.relpath(tdir, ROOT))
    say("  %d job(s), %d referenced script(s), README %s"
        % (len(jobs) if isinstance(jobs, dict) else 0, len(_referenced_scripts(doc)),
           "present" if os.path.exists(rd) else "MISSING"))
    for nte in notes:
        say("  · " + nte)
    if fails:
        say("\n%d PROBLEM(S) IN THE PACK-SIDE TEMPLATE:" % len(fails))
        for f in fails:
            say("  ❌ " + f)
        return 1
    say("\nPASS — the template parses, ships what it calls, and hides nothing.")
    return 0


# ---------------------------------------------------------------------------------------------
# selftest — every arm mutated on a COPY, never on the real template
# ---------------------------------------------------------------------------------------------

def selftest():
    fails, n = [], [0]

    def bite(name, ok, why=""):
        n[0] += 1
        if not ok:
            fails.append("[%s] %s" % (name, why))

    if _yaml() is None:
        print("COULD-NOT-ASK: the ci-template selftest — PyYAML is not importable, and every "
              "arm below parses YAML. Install it (pip install pyyaml).")
        return cna.EXIT

    bite("real/green", check(quiet=True) == 0,
         "the template as it stands must pass, or every mutation below proves nothing")

    tmp = tempfile.mkdtemp(prefix="ci-template-selftest-")
    try:
        def copy():
            d = tempfile.mkdtemp(dir=tmp)
            for f in (WORKFLOW, RUNNER, READMES):
                src = os.path.join(TEMPLATE_DIR, f)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(d, f))
            return d

        d = copy()
        bite("copy/green", check(d, quiet=True) == 0, "an untouched copy must still pass")

        # continue-on-error smuggled into a step
        d = copy()
        p = os.path.join(d, WORKFLOW)
        t = open(p).read().replace("      - name: Run the Apollo gates\n",
                                   "      - name: Run the Apollo gates\n"
                                   "        continue-on-error: true\n", 1)
        open(p, "w").write(t)
        bite("mutant/continue-on-error", check(d, quiet=True) == 1,
             "a smuggled continue-on-error must be RED")

        # a step that calls a script the pack does not carry
        d = copy()
        p = os.path.join(d, WORKFLOW)
        t = open(p).read().replace("ci-template/run-gates.py", "ci-template/not-shipped.py")
        open(p, "w").write(t)
        bite("mutant/missing-script", check(d, quiet=True) == 1,
             "a run: naming a file that does not exist must be RED")

        # broken YAML
        d = copy()
        p = os.path.join(d, WORKFLOW)
        open(p, "w").write(open(p).read() + "\n  : : not: yaml: [\n")
        bite("mutant/unparseable", check(d, quiet=True) == 1,
             "a template that does not parse must be RED")

        # a workflow with no trigger
        d = copy()
        p = os.path.join(d, WORKFLOW)
        t = open(p).read().replace("on:\n  push:\n  pull_request:\n", "")
        open(p, "w").write(t)
        bite("mutant/no-trigger", check(d, quiet=True) == 1,
             "a workflow with no `on:` never runs and must be RED")

        # the README quietly loses the promise it exists to make
        d = copy()
        p = os.path.join(d, READMES)
        open(p, "w").write(open(p).read().replace("Delete the step", "Remove it somehow"))
        bite("mutant/readme-loses-the-rule", check(d, quiet=True) == 1,
             "a README that stops naming the honest switch-off must be RED")

        # a runner that cannot recognise a refusal
        d = copy()
        p = os.path.join(d, RUNNER)
        open(p, "w").write(open(p).read().replace("77", "1"))
        bite("mutant/runner-forgets-77", check(d, quiet=True) == 1,
             "a runner with no 77 turns every refusal into a red and must be RED")

        # the runner stops compiling
        d = copy()
        p = os.path.join(d, RUNNER)
        open(p, "w").write("def broken(:\n")
        bite("mutant/runner-syntax", check(d, quiet=True) == 1,
             "a runner that does not compile must be RED")

        # nothing there at all is a REFUSAL, not a pass
        d = tempfile.mkdtemp(dir=tmp)
        bite("empty/refuses", cna.is_refusal(check(d, quiet=True)),
             "an absent template must refuse (77), never read as green")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("selftest: %d bites, %d fail(s)" % (n[0], len(fails)))
    for f in fails:
        print("  RED " + f)
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="validate the template (the default)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    sys.exit(check())


if __name__ == "__main__":
    main()
