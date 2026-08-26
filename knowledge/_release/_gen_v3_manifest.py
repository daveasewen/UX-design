#!/usr/bin/env python3
"""_gen_v3_manifest.py — the GENERATOR behind `designer-skills-v3/build-designer-pack.sh`.

WHY THIS EXISTS. `s219-D4(2)`: "THE EXACT CUT IS A PROPOSED MANIFEST FOR HIS EYE BEFORE THE
BAKE — release = explicit, versioned, Dave's word." A hand-kept ship list is the v1 defect the
v2 receipt names in its own words ("v1's copy-list had gone stale"): a copy-list typed by a
human ages against the tree that moved underneath it and nothing measures the gap. So the
manifest is GENERATED from a NAMED COMMIT — never from the working tree, never by hand — and
the bake reads the manifest rather than re-deriving the list a second time.

THE THREE JOBS (one file, three modes; the .sh is the only entry point a human drives):

  --manifest   enumerate the cut at <commit> into knowledge/_release/_v3_manifest.json
  --probe      import-probe every knowledge/_validate_*.py in an ISOLATED staging dir and
               write knowledge/_release/_v3_gate_probe.json (the gate verdict table)
  --stage      materialise the manifest's paths at <commit> into a dir (the bake's stage)
  --zip        deterministic zip of a stage dir (fixed mtimes, sorted order, fixed mode)
  --check      verify a baked pack against manifest + commit
  --selftest   the bites, mutation-tested

⛔ THE GATE VERDICTS ARE MEASURED, NOT READ BY EYE. `--probe` copies each validator plus its
LOCAL helper imports into a throwaway dir that contains ONLY the non-gate shipped set, then
RUNS it and classifies the exit. Reading a validator's import block by eye answers "what does
it import", which is not the question — the question is "does it RUN outside this repo", and
only a run answers that [[mutation-tests-the-clause-not-the-feature]]. The classifier:

  RUNNABLE        the gate reached a verdict (exit 0, or a clean non-zero FAIL with no
                  traceback) inside the staged pack
  NEEDS-DEP(x)    ModuleNotFoundError naming a third-party module `x`
  REPO-BOUND(why) it crashed reaching for something the pack does not ship — the offending
                  path is extracted from the traceback and named in the verdict

★ THE DIFFERENTIAL ARM — because a FAIL is not automatically a run. A gate that returns a
clean non-zero verdict inside the pack has demonstrably RUN; but its red may be caused by the
pack not carrying the thing it audits (`_validate_package_delta.py` audits `memento-package/`
against `knowledge/` — in a designer's project that subject does not exist, so its red is a
packaging artefact, not a finding). Reading the message and deciding by eye is exactly the
guess this module refuses. So every FAIL is re-run against a FULL-TREE stage of the same
commit and the two verdicts are compared:

  FAIL in pack + PASS in full tree  ⇒  REPO-BOUND (the pack does not carry its subject)
  FAIL in both                      ⇒  RUNNABLE (a live red, honestly declared, not a fence)

⛔ The full-tree run happens in a `git archive` STAGE under /var/tmp, never in the repo — a
validator that writes an audit file must not be allowed to dirty Dave's tree (#158 class).

⛔ DETERMINISM. The manifest carries NO timestamp. Its provenance is the commit sha, and the
build date it stamps into the pack README is the COMMIT's own date, not today's — a build-day
stamp would make two bakes of the same commit differ, which destroys the delta-audit this
whole shape exists to enable. `manifest_sha256` is the sha256 of the manifest file's bytes.

GATE-GLOB-SCOPE: this module reads the repo through `git ls-tree`/`git archive` at a named
commit and writes exactly two files under `knowledge/_release/`, plus whatever stage/zip path
it is explicitly given. It globs nothing else and widens no other gate's glob.

USAGE
    python3 knowledge/_release/_gen_v3_manifest.py --manifest --commit <sha>
    python3 knowledge/_release/_gen_v3_manifest.py --probe --commit <sha>
    python3 knowledge/_release/_gen_v3_manifest.py --stage <dir> --commit <sha>
    python3 knowledge/_release/_gen_v3_manifest.py --zip <stage> --out <zip> --commit <sha>
    python3 knowledge/_release/_gen_v3_manifest.py --check <zip> --commit <sha>
    python3 knowledge/_release/_gen_v3_manifest.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

VERSION = "v3.0.0"
SCHEMA = "apollo-designer-pack-manifest/1"
MANIFEST_PATH = os.path.join(HERE, "_v3_manifest.json")
PROBE_PATH = os.path.join(HERE, "_v3_gate_probe.json")

# ---------------------------------------------------------------------------------------------
# THE CUT — declared as include/exclude rules over the commit's tracked path list.
# Each group is (key, title, plain-words purpose, [rules]). A rule is a predicate over a path.
# Order matters: the FIRST group that claims a path owns it, so a path can never be double-counted.
# ---------------------------------------------------------------------------------------------

def _pfx(*prefixes):
    return lambda p: p.startswith(prefixes)


def _under(prefix, suffixes=None, not_under=(), not_base=()):
    def f(p):
        if not p.startswith(prefix):
            return False
        rest = p[len(prefix):]
        if any(rest.startswith(n) for n in not_under):
            return False
        b = os.path.basename(p)
        if b in not_base:
            return False
        if suffixes and not p.endswith(tuple(suffixes)):
            return False
        return True
    return f


# Design-facing runbooks: the ones a designer building with Apollo actually opens.
# The Memento-internal ones (capture-ritual, git-commit, context-gauge, parallel-conductor,
# dream-pass, decision-audit) are NOT here — see MEMENTO_RUNBOOK_CALL in the manifest notes.
DESIGN_RUNBOOKS = [
    "_RUNBOOK-compose-from-canon.md",
    "_RUNBOOK-gated-component.md",
    "_RUNBOOK-render-verify.md",
    "_RUNBOOK-criteria-contract.md",
    "_RUNBOOK-consult.md",
    "_RUNBOOK-onboard-code-library.md",
    "_RUNBOOK-review-doc.md",
    "_RUNBOOK-toolkit-tranche.md",
    "_RUNBOOK-reconcile-dark-tokens.md",
    "_RUNBOOK-external-claims.md",
    "_RUNBOOKS.md",
]

# Explicitly NOT shipped with the design half. Memento's own half ships none of these either:
# memento-package/ carries machinery only (5 files + the manifest), no runbooks at all — so the
# clean cut MIRRORS that choice and these stay repo-side. Named so the omission is auditable.
MEMENTO_INTERNAL_RUNBOOKS = [
    "_RUNBOOK-capture-ritual.md",
    "_RUNBOOK-git-commit.md",
    "_RUNBOOK-context-gauge.md",
    "_RUNBOOK-parallel-conductor.md",
    "_RUNBOOK-dream-pass.md",
    "_RUNBOOK-decision-audit.md",
    "_RUNBOOK-densify-adversarial.md",
]

# The local (in-repo) modules each validator needs. MEASURED by AST at probe time, not typed —
# this constant is only the seed for the stage: helpers live beside the gates in knowledge/.
HELPER_HOMES = {
    "gen_theme_cascade": "knowledge/canon/gen_theme_cascade.py",
}

# Data files the gates read that are NOT part of any other group but must ride with the gates
# for them to have anything to check. Verdict-driven: only the ones the probe proves are needed.
GATE_DATA_CANDIDATES = [
    "knowledge/_assertions.json",
    "knowledge/_ASSERTIONS.md",
    "knowledge/_binds-ratchet.json",
    "knowledge/_type_ratchet.json",
    "knowledge/_TOKEN-FORK-LEDGER.json",
    "knowledge/component-types.json",
    "knowledge/chart-intents.json",
    "knowledge/canon/_type-bindings.json",
    "knowledge/canon/_bindings-applied.json",
]

EXCLUDED = [
    ("reviews/", "Dave's review surfaces — this session's thinking, not the engine. s219-D4(1): "
                 "'without all the review files and extras'."),
    ("notes/", "Briefs, receipts and filed sub-reports — the workshop's paperwork."),
    ("runs/", "Session run logs — state, not machinery."),
    ("archive/", "Retired material, kept for history only."),
    ("projects/", "Client project work — not the design system."),
    ("system-manager/", "A strand project, not Apollo."),
    ("second-system-govuk/", "A strand project, not Apollo."),
    ("digital-experience-transformation/", "A strand project, not Apollo."),
    ("knowledge/assets/fonts/", "LICENCE. Only the _desktop set ships (see the library group); "
                                "any webfont pack is outside the licence we hold."),
    ("knowledge/assets/photography/", "LICENCE. Getty/EyeEm stock originals — non-repo already."),
    ("knowledge/assets/photography-web/", "LICENCE. Getty/EyeEm derivatives — redistribution is "
                                          "not covered."),
    ("knowledge/tokens/_raw/", "ADR-0005: raw Figma exports are client assets, untracked."),
    ("API-KEY.txt", "Secret."),
    (".token-cache.json", "Secret."),
    ("GOOD-MORNING.md", "Dave's session state. s219-D4(1): state, not machinery."),
    ("_LIVE-STATE.md", "Dave's session state."),
    ("_CHAIN.md", "Dave's session state."),
    ("knowledge/_state.json", "Dave's task store — his items, not a designer's."),
    ("knowledge/_rulings.json", "Apollo's ruling store — Dave's record."),
    ("knowledge/_SESSIONS.jsonl", "Session state."),
    ("knowledge/_memento-index.json", "Generated from Apollo's own record; adopters regenerate "
                                      "(memento-package machinery manifest says so verbatim)."),
    ("designer-skills-v1/", "FROZEN release, s114-D4."),
    ("designer-skills-v2/", "FROZEN release, s114-D4. Its four SKILL.md were the REFERENCE for "
                            "the v3 refresh, not the source — v3 ships its own five from "
                            "designer-skills-v3/skills/ (#219 R3)."),
]


def groups():
    """The ordered group table. First match owns the path."""
    return [
        dict(key="engine-canon.tokens", group="engine-canon", title="Tokens",
             plain="Every design token you work from — colour, type, spacing, elevation, "
                   "motion, the four theme override sets and the palettes.",
             match=_under("knowledge/tokens/", not_under=("_raw/",),
                          not_base=("EXAMPLE-tokens.json",))),
        dict(key="engine-canon.components", group="engine-canon", title="Component contracts",
             plain="One .meta.json per component: props, variants, token bindings, states, "
                   "anti-patterns, accessibility. Plus the schema they validate against.",
             match=lambda p: p.startswith("knowledge/components/")
                             and not os.path.basename(p).startswith("EXAMPLE-")),
        dict(key="engine-canon.snippets", group="engine-canon", title="Reference markup",
             plain="The reviewed HTML for each component — what 'correct' looks like.",
             match=lambda p: p.startswith("knowledge/snippets/")
                             and not os.path.basename(p).startswith("EXAMPLE-")),
        dict(key="engine-canon.canon", group="engine-canon", title="Canon CSS + its generators",
             plain="canon.css and type.css (the composition layer), the data-vis behaviour JS, "
                   "the type bindings, and the generators that mint canon from tokens.",
             match=_under("knowledge/canon/", not_under=("__pycache__/",))),
        dict(key="engine-canon.compliance", group="engine-canon", title="Compliance graph",
             plain="Which WCAG criteria apply to which component, plus the rule set.",
             match=_under("knowledge/compliance/", not_under=("_vendor/",),
                          not_base=("EXAMPLE-contrast-rule.json",))),
        dict(key="engine-canon.icons", group="engine-canon", title="Icon library",
             plain="The real glyphs. Skills must use these and never invent an icon — the v2 "
                   "pack shipped them for exactly that reason.",
             match=_under("knowledge/assets/icons/", not_base=())),
        dict(key="engine-canon.logos", group="engine-canon", title="Brand marks",
             plain="The hexagon and masterbrand SVGs, light/dark, colour/mono.",
             match=_under("knowledge/assets/logos/")),
        dict(key="engine-canon.guidelines", group="engine-canon", title="Design guidelines",
             plain="The written standards a designer consults — brand, colour, type, tone, "
                   "accessibility, component standards.",
             match=_under("knowledge/guidelines/")),

        dict(key="gates", group="gates", title="Runnable gates",
              plain="The executable checks. Each one below was RUN in an isolated copy of this "
                   "pack to find out whether it works away from this repo — the verdicts are "
                   "measured, not guessed.",
             match=lambda p: (p.startswith("knowledge/_validate_")
                              or p.startswith("knowledge/_gate_")) and p.endswith(".py")),

        dict(key="runbooks", group="runbooks", title="Runbooks",
             plain="The design-facing procedures: how to compose from canon, how to take a "
                   "component through its gates, how to render and verify, how to write a "
                   "criteria contract, how to onboard an existing code library.",
             match=lambda p: os.path.dirname(p) == "knowledge"
                             and os.path.basename(p) in DESIGN_RUNBOOKS),

        dict(key="library.showroom", group="library", title="Showroom",
             plain="The live library: every component page, the foundations pages (bento, "
                   "grids, logos, photography), the thumbnails and the index.",
             match=_under("showroom/")),
        dict(key="library.rails", group="library", title="Edit-pass rails manifest",
             plain="The one generated file the library, the editor and the generator all read, "
                   "so none of them can drift (s219-D3(6)).",
             match=lambda p: p == "knowledge/_render/_bento_edit_rails.json"),
        dict(key="library.render", group="library", title="Render machinery",
             plain="render.py — the proven headless-Chromium shape, so a designer can see their "
                   "own work the way Dave does.",
             match=lambda p: p == "knowledge/_render/render.py"),
        dict(key="library.fonts", group="library", title="Desktop fonts",
             plain="The licensed desktop cut, so the library renders in the real face. "
                   "LICENCE QUESTION — see the open questions.",
             match=_under("knowledge/assets/fonts/_desktop/")),

        dict(key="memento", group="memento-clean-cut", title="Memento machinery",
             plain="A clean cut of Memento — the chain generator, retrieval, the graph edges, "
                   "the gauge shim, the consult lexicon. Machinery only, no record: every "
                   "adopting project grows its own chain.",
             match=lambda p: p.startswith("memento-package/machinery/")
                             and "__pycache__" not in p),
        dict(key="memento.docs", group="memento-clean-cut", title="Memento docs",
             plain="What Memento is, and the boot rule.",
             match=lambda p: p in ("memento-package/WHAT-MEMENTO-IS.md",
                                   "memento-package/README.md")),
        dict(key="memento.plugin", group="memento-clean-cut", title="Memento Claude plugin",
             plain="The packaged plugin — the boot skill and its reference.",
             match=lambda p: p.startswith("memento-package/claude-plugin/")
                             and "__pycache__" not in p and not p.endswith(".zip")),

        # #219 seam 7, on R3's Q1: the skills group ships R3's OWN five, not v2's four. Until this
        # was repointed the pack shipped v2's skills and none of the refreshed set — the whole
        # point of s219-D4(4). ⚠ FUNCTION OF THE COMMIT like every other path: at a commit before
        # designer-skills-v3/skills/ is tracked this claims NOTHING and the group is empty.
        dict(key="skills", group="skills", title="Skills",
             plain="The five v3 skills: four refreshed against this knowledge base and the new "
                   "gate-runner that runs the packed gates on a designer's own work.",
             match=lambda p: p.startswith("designer-skills-v3/skills/")
                             and p.endswith("/SKILL.md")),
    ]


# ---------------------------------------------------------------------------------------------
# git plumbing — every read is at a NAMED COMMIT
# ---------------------------------------------------------------------------------------------

def git(*args, cwd=None, binary=False):
    r = subprocess.run(["git"] + list(args), cwd=cwd or ROOT,
                       capture_output=True, check=False)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.decode()[:400]))
    return r.stdout if binary else r.stdout.decode()


def resolve_commit(ref):
    return git("rev-parse", ref).strip()


def commit_date(sha):
    """The COMMIT's own date, ISO, UTC. Used for the README stamp and the zip mtimes so two
    bakes of the same commit are byte-identical [[measure-dont-convert-units]]."""
    return git("show", "-s", "--format=%cI", sha).strip()


def commit_epoch(sha):
    return int(git("show", "-s", "--format=%ct", sha).strip())


def tree_paths(sha):
    out = git("ls-tree", "-r", "--name-only", sha)
    return [l for l in out.split("\n") if l]


def blob_sizes(sha, paths):
    """One batch call — `git cat-file --batch-check` over the named blobs."""
    if not paths:
        return {}
    inp = "".join("%s:%s\n" % (sha, p) for p in paths)
    r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=ROOT,
                       input=inp.encode(), capture_output=True, check=True)
    sizes = {}
    for path, line in zip(paths, r.stdout.decode().strip().split("\n")):
        parts = line.split()
        sizes[path] = int(parts[2]) if len(parts) >= 3 and parts[1] == "blob" else 0
    return sizes


def blob_shas(sha, paths):
    if not paths:
        return {}
    inp = "".join("%s:%s\n" % (sha, p) for p in paths)
    r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=ROOT,
                       input=inp.encode(), capture_output=True, check=True)
    out = {}
    for path, line in zip(paths, r.stdout.decode().strip().split("\n")):
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "blob":
            out[path] = parts[0]
    return out


def is_dirty():
    return bool(git("status", "--porcelain").strip())


# ---------------------------------------------------------------------------------------------
# THE GATE PROBE — measured, in an isolated dir
# ---------------------------------------------------------------------------------------------

STD = set(sys.stdlib_module_names)


def local_imports(src_text, knowledge_files):
    """AST scan for imports that resolve to a module living in knowledge/. Used to decide what
    to COPY into the probe stage — never to decide the verdict."""
    mods = set()
    try:
        t = ast.parse(src_text)
    except SyntaxError:
        return set(), set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                mods.add(n.module.split(".")[0])
    local = {m for m in mods if (m + ".py") in knowledge_files or m in HELPER_HOMES}
    third = {m for m in mods if m not in STD and m not in local}
    return local, third


TRACE = "Traceback (most recent call last)"
# ★ Widened deliberately: a well-mannered gate CATCHES its ImportError and prints a courteous
# refusal instead of a traceback (`_validate_state_contrast.py` prints COULD-NOT-ASK). Matching
# only `ModuleNotFoundError:` would call those RUNNABLE and hide a real dependency
# [[unmatched-grep-is-not-an-absence]] — the needle is the phrase, not the exception class.
MODNOTFOUND = re.compile(r"No module named [\"']([^\"']+)[\"']")
PATHERR = re.compile(r"(?:FileNotFoundError|NotADirectoryError|IsADirectoryError)[^\n]*?"
                     r"'([^']+)'")
# A gate that refuses for want of an ARGUMENT has run perfectly well; it just wants a target.
ARGS_REFUSAL = re.compile(r"no input files|Pass paths or --all|need at least one|"
                          r"REFUSED: need", re.I)
# A green that graded nothing. The gate's own count, in the gate's own words.
# ⚠ INPUT nouns only. The first cut matched any `0 <word>(s)` and therefore read "135
# snippet(s), 0 failure(s)" — a gate that graded 135 files and found nothing wrong — as a
# vacuous pass. Zero FAILURES is the good news; zero FILES is the empty subject. Different
# nouns, opposite meanings [[measure-dont-convert-units]].
EMPTY_POP = re.compile(r"\b(?:0|no) (?:[a-z\-]+ )?"
                       r"(?:file|snippet|page|component|token|doc|rule|path|meta|specimen|"
                       r"artefact|item|tranche|css|html)\(s\)")
# THE SUBJECT TEST, anchored. A failure message mentions plenty of paths — the glob it scanned,
# the files it graded, the rule it cites. Only the paths in a MISSING-language clause answer the
# packaging question, so the sentence context is part of the needle: matching bare path-shapes
# called `_validate_token_forks.py` repo-bound off the line "glob: knowledge/canon/*.css", which
# is the file it successfully READ [[unmatched-grep-is-not-an-absence]], other direction.
MISSING_LINE = re.compile(r"does not exist|not found|cannot read|no such file|UNPARSEABLE|"
                          r"missing|nothing to check|could not (?:find|read|open)", re.I)
PATHISH = re.compile(r"((?:knowledge|showroom|reviews|notes|runs|memento-package|"
                     r"designer-skills-v[12]|projects|archive)/[A-Za-z0-9_.\-]+"
                     r"(?:/[A-Za-z0-9_.\-]+)*"
                     r"|GOOD-MORNING\.md|_LIVE-STATE\.md|_CHAIN\.md|_rulings\.json|_state\.json)")


def classify(rc, out, err, shipped):
    """The verdict classifier. Reads the RUN, never the source."""
    blob = (out or "") + "\n" + (err or "")
    if rc == 124:
        return "REPO-BOUND", "timed out in the staged pack (>%ds) — it is walking something " \
                             "the pack does not carry" % PROBE_TIMEOUT
    m = MODNOTFOUND.search(blob)
    if m:
        name = m.group(1).split(".")[0]
        if name in STD:
            return "REPO-BOUND", "stdlib module %r unavailable — environment, not the pack" % name
        return "NEEDS-DEP", name
    if TRACE in blob:
        pm = PATHERR.search(blob)
        if pm:
            missing = pm.group(1)
            short = missing.replace(os.sep, "/")
            for s in shipped:
                if short.endswith(s):
                    return "RUNNABLE", "reached a verdict (path error inside the shipped set)"
            return "REPO-BOUND", "reaches for %s, which the pack does not ship" % _tail(short)
        first = [l for l in blob.strip().split("\n") if l.strip()]
        return "REPO-BOUND", "crashed: %s" % (first[-1][:160] if first else "unknown")
    if rc == 0:
        return "RUNNABLE", "ran clean, verdict PASS"
    if ARGS_REFUSAL.search(blob):
        return "RUNNABLE", "runs; it wants an explicit target and refuses without one — a " \
                           "stated contract, not a fence"
    # THE SUBJECT TEST. A clean FAIL is a verdict — unless the message says the thing it went
    # looking for is not in the pack. That is a packaging fact, and it is readable mechanically.
    outside = []
    for line in blob.split("\n"):
        if not MISSING_LINE.search(line):
            continue
        for p in PATHISH.findall(line):
            if p not in shipped and "*" not in p:
                outside.append(p)
    if outside:
        return "REPO-BOUND", "runs, but its verdict is about %s, which the pack does not ship" \
                             % _tail(outside[0])
    return "RUNNABLE", "ran, verdict FAIL (exit %d) — a verdict is a run" % rc


def _tail(p, n=3):
    """Name the path the way the DESIGNER will see it, not the way the probe staged it.
    The probe extracts into <tmp>/pack/, so a raw traceback path reads
    `/var/tmp/v3probe-xxxx/pack/knowledge/_state.json` — and `pack/knowledge/_state.json` on
    Dave's page is a directory that exists nowhere. Strip the stage, keep the repo path."""
    if "/pack/" in p:
        p = p.split("/pack/")[-1]
    parts = [x for x in p.split("/") if x]
    return "/".join(parts[-n:]) if len(parts) > n else p


PROBE_TIMEOUT = 25


def probe_gates(sha, stage_root=None, only=None, verbose=False, full_stage=None):
    """Materialise the non-gate shipped set in a throwaway dir, then RUN each gate in it."""
    paths = tree_paths(sha)
    tbl = groups()
    claimed = {}
    for p in paths:
        for g in tbl:
            if g["match"](p):
                claimed.setdefault(g["key"], []).append(p)
                break
    gate_paths = sorted(claimed.get("gates", []))
    non_gate = sorted(p for k, v in claimed.items() if k != "gates" for p in v)

    knowledge_files = {os.path.basename(p) for p in paths if os.path.dirname(p) == "knowledge"}

    tmp = stage_root or tempfile.mkdtemp(prefix="v3gateprobe-", dir="/var/tmp")
    stage = os.path.join(tmp, "pack")
    if not os.path.isdir(stage):
        os.makedirs(stage, exist_ok=True)
        extract(sha, non_gate + GATE_DATA_CANDIDATES, stage, tolerant=True)

    shipped = set(non_gate)
    results = []
    for gp in gate_paths:
        base = os.path.basename(gp)
        if only and base not in only:
            continue
        src = git("show", "%s:%s" % (sha, gp))
        loc, third = local_imports(src, knowledge_files)
        # copy the gate + its local helper closure into the stage
        copied = [gp]
        frontier = set(loc)
        seen = set()
        while frontier:
            m = frontier.pop()
            if m in seen:
                continue
            seen.add(m)
            home = HELPER_HOMES.get(m, "knowledge/%s.py" % m)
            if home in paths:
                copied.append(home)
                l2, _ = local_imports(git("show", "%s:%s" % (sha, home)), knowledge_files)
                frontier |= (l2 - seen)
        extract(sha, copied, stage, tolerant=True)

        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR="/var/tmp",
                   PYTHONPATH=os.path.join(stage, "knowledge"))
        r = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp],
                           cwd=stage, capture_output=True, env=env)
        out, err = r.stdout.decode("utf8", "replace"), r.stderr.decode("utf8", "replace")
        invocation = ""
        if "REFUSED (write-gate)" in out + err:
            invocation = "--write"
        elif ARGS_REFUSAL.search(out + err) and "--all" in (out + err):
            invocation = "--all"
        if invocation:
            r = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp, invocation],
                               cwd=stage, capture_output=True, env=env)
            out, err = r.stdout.decode("utf8", "replace"), r.stderr.decode("utf8", "replace")
        verdict, why = classify(r.returncode, out, err, shipped)
        # ⛔ THE VACUOUS-PASS ARM. `_validate_no_hardcode.py` exits 0 with "passed (0 tranche
        # file(s))" — it graded NOTHING and called it green. In the pack that is correct and
        # expected (the tranche dir is the DESIGNER's work, which does not exist yet), but a
        # green that graded zero must never be presented as a green that graded something
        # [[green-tests-cannot-see-scope]]. So the population is measured from the gate's own
        # output and DECLARED beside its verdict.
        population = ""
        if verdict == "RUNNABLE" and r.returncode == 0:
            population = "EMPTY-IN-PACK" if EMPTY_POP.search(out + err) else "graded"
        fail_head = ""
        differential = ""
        if verdict == "RUNNABLE" and r.returncode != 0:
            lines = [l.strip() for l in (out + "\n" + err).split("\n") if l.strip()]
            fail_head = " / ".join(lines[:3])[:300]
            if full_stage:
                fr = subprocess.run(
                    ["timeout", str(PROBE_TIMEOUT), sys.executable, gp]
                    + ([invocation] if invocation else []),
                    cwd=full_stage, capture_output=True,
                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR="/var/tmp",
                             PYTHONPATH=os.path.join(full_stage, "knowledge")))
                fout = (fr.stdout + fr.stderr).decode("utf8", "replace")
                if fr.returncode == 0:
                    differential = "full-tree PASS"
                    verdict = "REPO-BOUND"
                    why = ("runs, but its subject is not in the pack — it is GREEN against the "
                           "full repo and RED here: " + (fail_head[:140] or "no message"))
                elif TRACE in fout:
                    differential = "full-tree CRASH"
                else:
                    differential = "full-tree FAIL too"
                    why = ("ran, verdict FAIL in the pack AND in the full repo — a live red, "
                           "not a packaging fence: " + (fail_head[:140] or "no message"))

        # the selftest arm — does the gate prove it can BITE without repo data?
        st = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp, "--selftest"],
                            cwd=stage, capture_output=True, env=env)
        sout = (st.stdout + st.stderr).decode("utf8", "replace")
        if "unrecognized" in sout or "usage:" in sout.lower() and st.returncode == 2:
            selftest = "none"
        elif st.returncode == 0:
            selftest = "green"
        elif TRACE in sout or "No module named" in sout:
            selftest = "crashed"
        else:
            selftest = "red"

        results.append(dict(
            gate=base, path=gp, verdict=verdict, why=why,
            third_party=sorted(third), local_imports=sorted(seen),
            invocation=invocation, selftest=selftest, exit=r.returncode,
            fail_head=fail_head, differential=differential, population=population,
        ))
        if verbose:
            print("%-42s %-12s %s" % (base, verdict, why), flush=True)
    return dict(commit=sha, timeout_s=PROBE_TIMEOUT, gates=results), tmp


def extract(sha, paths, dest, tolerant=False):
    """git archive the named paths at the named commit into dest. Bytes come from the COMMIT."""
    paths = [p for p in paths if p]
    if not paths:
        return
    if tolerant:
        have = set(tree_paths(sha))
        paths = [p for p in paths if p in have]
        if not paths:
            return
    os.makedirs(dest, exist_ok=True)
    for i in range(0, len(paths), 400):
        chunk = paths[i:i + 400]
        ar = subprocess.run(["git", "archive", "--format=tar", sha, "--"] + chunk,
                            cwd=ROOT, capture_output=True)
        if ar.returncode != 0:
            raise RuntimeError("git archive failed: " + ar.stderr.decode()[:400])
        tr = subprocess.run(["tar", "-x", "-C", dest], input=ar.stdout, capture_output=True)
        if tr.returncode != 0:
            raise RuntimeError("tar failed: " + tr.stderr.decode()[:400])


# ---------------------------------------------------------------------------------------------
# THE MANIFEST
# ---------------------------------------------------------------------------------------------

OPEN_QUESTIONS = [
    dict(id="Q1", title="Memento ships machinery with no store — does v3 hand designers an "
                        "EMPTY record to fill?",
         body="I checked, because the brief asked. memento-package ships five machinery files "
              "and a lexicon, and it ships no record at all — no chain, no rulings store, no "
              "task store, not even an empty one. Its own manifest says why: every adopting "
              "project grows its own chain.||"
              "Mirroring that exactly means a designer unzips v3, says good morning, and "
              "Memento has nowhere to write.||"
              "The proposal, if you want them productive on day one: ship three empty stores "
              "with the right shape and nothing inside. A task store holding an empty list. A "
              "rulings store holding an empty list. And no chain file at all — its absence is "
              "the signal the boot rule reads to know this is a new project.||"
              "An empty shape is machinery. A filled shape is your record. The line you drew "
              "holds either way. The only question is whether the designer types the first "
              "brace or we do.",
         options=["Mirror memento exactly — no stores, the pack's first run creates them",
                  "Ship the three empty store shapes (recommended)",
                  "Ship empty stores AND a starter _CHAIN.md explaining the first move"]),
    dict(id="Q2", title="Do the licensed desktop fonts travel in the zip?",
         body="The library only looks like Apollo in the real face. The desktop cut is tracked "
              "in this repo on purpose — the .gitignore says why: the repo is private and "
              "shared only in-licence.||"
              "A zip on GitHub is a wider audience than the repo. If your designers sit inside "
              "the same licence, the fonts ride along and the showroom renders correctly. If "
              "they do not, the pack ships without them and the library falls back to a stock "
              "face. It still works. It does not look right.||"
              "Eight of the thirty-four megabytes are the fonts, so this is also the single "
              "biggest lever on download size.",
         options=["Ship the desktop fonts (54 files) — designers are in-licence",
                  "Leave the fonts out and note the fallback in the pack README"]),
    dict(id="Q3", title="Do the canon GENERATORS ship, or only the canon they produce?",
         body="The canon folder holds canon.css and type.css — and the four generators that "
              "mint them from the tokens.||"
              "v2 shipped the stylesheets only: a baked reference that nobody regenerates. You "
              "asked for as close to what you use as possible, and what you use is the "
              "generator.||"
              "Shipping them means a designer can change a token and re-mint canon. It also "
              "means they can produce canon that never passed a gate. The gates are in the "
              "pack too, which is why I lean towards shipping them.",
         options=["Ship the generators (v3 is the working engine — recommended, the gates are "
                  "in the pack too)",
                  "Ship the minted CSS only, v2-style"]),
    dict(id="Q4", title="Which runbooks are design-facing and which are yours?",
         body="Eleven runbooks are proposed in, as design-facing. Seven are held out as your "
              "own working ritual: capture, git commit, the context gauge, the parallel "
              "conductor, the dream pass, decision audit, densify-adversarial.||"
              "memento-package itself ships no runbooks at all — machinery only — so mirroring "
              "it holds all seven out, and that is what the list currently does.||"
              "One is awkward. Capture is the ritual that makes Memento work. A designer with "
              "the machinery and no capture ritual has a chain that never grows.",
         options=["Hold all seven out (mirrors memento-package exactly)",
                  "Send capture-ritual across with the Memento half (recommended)",
                  "Send capture-ritual and context-gauge across"]),
    # ---------------------------------------------------------------------------------------
    # #219 seam 7, on R2's Q1 (and R3's Q6 — the two lanes found the same thing from opposite
    # ends and both asked for a card). Dave is shown "39 gates that run anywhere" a few inches
    # further up this page. FOUR OF THEM ARRIVE RED, on a fresh unzip, before the designer has
    # written a line. That was in two filed reports and nowhere on his surface. This card
    # DECIDES NOTHING — deliberately no option is marked recommended, because which way this
    # goes is a positioning call about the first thing an outside designer ever sees.
    # ⚠ The four gate names below are checked against the repo by a selftest bite: a renamed
    # gate must break the bite rather than leave this card quietly lying (R3's finding 9).
    dict(id="Q5", title="Four of the packed gates are RED the day the pack is unzipped. "
                        "Ship them anyway, or clear them first?",
         body="Measured, not guessed — the gates were run out of an extracted pack from a "
              "directory that is not this repo, twice, by two different lanes: 32 pass, 4 fail. "
              "None of the four has anything to do with a designer's work. They are Apollo's "
              "own open reds at the commit the pack is cut from.||"
              "_validate_evidence.py — exits 2, which is bad arguments rather than a verdict. "
              "It needs a rows file handed to it and the pack's runner gives it none, so as the "
              "pack invokes it, it can never pass.||"
              "_validate_token_forks.py — three token forks are not in the ledger.||"
              "_validate_type_blast_radius.py — one selector, .search input, has escaped its "
              "declared radius.||"
              "_validate_type_composites.py — 664 composite violations inside the pack, 1,091 "
              "in this repo. That is the standing type-composite debt, which by your own ratchet "
              "may only ever shrink.||"
              "Why it matters more than the number looks: a designer unzips the pack, runs the "
              "gates exactly as the README and the new gate-runner skill tell them to, and is "
              "met with hundreds of violations they did not cause. The likely conclusion is that "
              "the gates are noise — and that conclusion is formed on day one and does not get "
              "revisited.||"
              "The middle option exists and works: a baseline file records today's reds so only "
              "the DIFFERENCE is the designer's, and the reds are still printed rather than "
              "hidden. It is built and mutation-tested, and it is deliberately NOT wired on, "
              "because switching it on is a decision about what the pack claims, not a "
              "mechanical default.",
         options=["Fix the four before the bake — cut v3 from a commit whose own gates are green",
                  "Ship them with the baseline switched on — reds recorded, printed, and only "
                  "new ones fail the designer's build",
                  "Ship them red and documented — the pack README names the four, the skill "
                  "tells designers to subtract them"]),
]

# The four gates named in Q5's body. Held as data so the selftest can prove they still exist:
# a card that names a renamed gate is the read-chain-staleness class, and it would go stale
# silently on Dave's own decision surface. [[no-gate-parses-the-artefact]]
Q5_RED_GATES = ["_validate_evidence.py", "_validate_token_forks.py",
                "_validate_type_blast_radius.py", "_validate_type_composites.py"]


def build_manifest(sha, probe):
    paths = tree_paths(sha)
    tbl = groups()
    claimed = {}
    for p in paths:
        for g in tbl:
            if g["match"](p):
                claimed.setdefault(g["key"], []).append(p)
                break

    verdicts = {r["gate"]: r for r in probe["gates"]}
    runnable = sorted(r["path"] for r in probe["gates"] if r["verdict"] == "RUNNABLE")
    needsdep = sorted(r["path"] for r in probe["gates"] if r["verdict"] == "NEEDS-DEP")
    repobound = sorted(r["path"] for r in probe["gates"] if r["verdict"] == "REPO-BOUND")

    # The gates group SHIPS the runnable ones plus the needs-dep ones (a named pip install is
    # a documented prerequisite, not a fence). Repo-bound gates are OUT, each with its reason.
    ship_gates = runnable + needsdep
    helper_closure = sorted({h for r in probe["gates"] if r["verdict"] in ("RUNNABLE", "NEEDS-DEP")
                             for m in r["local_imports"]
                             for h in [HELPER_HOMES.get(m, "knowledge/%s.py" % m)]
                             if h in paths})
    gate_data = [p for p in GATE_DATA_CANDIDATES if p in paths]

    # ---- THE CI TEMPLATE RIDES WITH THE GATES (#219 R2, s219-D4(3)). ---------------------------
    # The pack-side half of "CI both halves" is a workflow a designer copies into their own repo,
    # plus the runner it calls and a README that says what blocks and how to turn a check off
    # honestly. It belongs to the GATES group and not to a group of its own, deliberately: a
    # workflow that runs the gates is not a seventh thing to explain to Dave, it is how the gates
    # get run. ⚠ IT IS A FUNCTION OF THE COMMIT LIKE EVERY OTHER PATH — at a commit where
    # designer-skills-v3/ci-template/ does not yet exist this list is EMPTY and the manifest's
    # bytes are unchanged, which is exactly why adding this rule did not invalidate the manifest
    # R1 generated. It starts shipping at the commit that lands the files.
    ci_template = sorted(p for p in paths if p.startswith("designer-skills-v3/ci-template/"))

    # Every path is owned by exactly ONE group. The gates group pulls in helper modules and data
    # files that other groups may already own (canon/_type-bindings.json is engine-canon's, and
    # the type gates read it) — without this the totals would count them twice and the pack size
    # on Dave's page would be a number nothing produced [[measure-dont-convert-units]].
    already = set()
    out_groups = []
    seen_group = {}
    for g in tbl:
        ps = sorted(claimed.get(g["key"], []))
        if g["key"] == "gates":
            ps = sorted(set(ship_gates) | set(helper_closure) | set(gate_data) | set(ci_template))
        ps = [p for p in ps if p not in already]
        already.update(ps)
        sizes = blob_sizes(sha, ps)
        entry = dict(key=g["key"], group=g["group"], title=g["title"], plain=g["plain"],
                     files=len(ps), bytes=sum(sizes.values()), paths=ps)
        if g["key"] == "gates":
            entry["verdicts"] = [dict(gate=r["gate"], verdict=r["verdict"], why=r["why"],
                                      selftest=r["selftest"],
                                      third_party=r["third_party"],
                                      population=r.get("population", ""),
                                      invocation=r["invocation"])
                                 for r in sorted(probe["gates"], key=lambda x: x["gate"])]
            entry["counts"] = dict(
                runnable=len(runnable), needs_dep=len(needsdep), repo_bound=len(repobound),
                empty_population=sum(1 for r in probe["gates"]
                                     if r.get("population") == "EMPTY-IN-PACK"))
            # Emitted ONLY when the files exist at this commit — an empty key would change the
            # manifest's bytes for every commit before the template landed, and a ship list has
            # to be a function of the tree, not of when the generator was edited.
            if ci_template:
                entry["ci_template"] = ci_template
        if g["key"] == "skills":
            # #219 seam 7: the placeholder slot is FILLED. R3 shipped the gate-runner as
            # `check-with-gates` (its pairing with check-against-design-system is the pedagogy:
            # the mechanical half and the reading half), so the named-empty-slot emission is gone
            # rather than left to promise a file that now exists under a different name.
            entry["status"] = "refreshed at #219 R3 — four rewritten against this KB, one new"
        out_groups.append(entry)
        seen_group.setdefault(g["group"], []).append(entry)

    totals = dict(
        files=sum(e["files"] for e in out_groups),
        bytes=sum(e["bytes"] for e in out_groups),
        by_group={gk: dict(files=sum(e["files"] for e in es),
                           bytes=sum(e["bytes"] for e in es))
                  for gk, es in seen_group.items()},
    )

    excluded = [dict(path=p, reason=r) for p, r in EXCLUDED]
    excluded.append(dict(
        path="knowledge/_validate_* (repo-bound subset)",
        reason="MEASURED, not assumed: %d validators crashed reaching for something the pack "
               "does not carry. Each is named with its reason in the gates group's verdict "
               "table." % len(repobound)))
    excluded.append(dict(
        path="knowledge/ (everything else)",
        reason="The audit files, build scripts, session machinery and working documents that "
               "make up the rest of knowledge/ — the workshop, not the engine."))

    return dict(
        schema=SCHEMA,
        version=VERSION,
        status="PROPOSED — awaiting Dave's word (s219-D4(2): release = his word)",
        commit=sha,
        commit_date=commit_date(sha),
        ruling="s219-D4",
        groups=out_groups,
        excluded=excluded,
        open_questions=OPEN_QUESTIONS,
        totals=totals,
        gate_probe=dict(timeout_s=probe["timeout_s"],
                        commit=probe["commit"],
                        repo_bound=[dict(gate=r["gate"], why=r["why"])
                                    for r in sorted(probe["gates"], key=lambda x: x["gate"])
                                    if r["verdict"] == "REPO-BOUND"]),
    )


def canonical(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def manifest_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def all_paths(man):
    out = []
    for g in man["groups"]:
        out.extend(g["paths"])
    return sorted(set(out))


# ---------------------------------------------------------------------------------------------
# THE PAGE — Dave's go/no-go surface. GENERATED from the manifest, never hand-kept: a page that
# said 1,590 files while the manifest said something else is the exact defect v3 exists to end.
# Two-register rule (_RUNBOOK-review-doc.md, ruled #66-D5): plain prose leads every card, the
# machinery folds beneath it. Dave is dyslexic — one group per card, one idea per sentence.
# ---------------------------------------------------------------------------------------------

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def mb(n):
    if n >= 1_000_000:
        return "%.1f MB" % (n / 1_000_000)
    if n >= 1000:
        return "%d KB" % round(n / 1000)
    return "%d bytes" % n


PAGE_CSS = """
  :root{ --pg:#FFFFFF; --pgink:#1A1A1A; --pgmut:#626262; --pgline:#E1E1E1; --pgsoft:#F5F5F5; }
  body{margin:0; padding:40px 32px 120px; background:var(--pg); color:var(--pgink);
       font-family:var(--typography-font-family, system-ui, -apple-system, "Segoe UI", sans-serif);
       -webkit-font-smoothing:antialiased; line-height:1.55;}
  .wrap{max-width:1180px; margin:0 auto;}
  h1{font-size:28px; line-height:1.2; margin:0 0 6px; letter-spacing:-.01em;}
  h2{font-size:20px; margin:56px 0 4px; letter-spacing:-.01em;}
  h3{font-size:15px; margin:28px 0 8px; text-transform:uppercase; letter-spacing:.08em; color:var(--pgmut);}
  p{margin:8px 0 14px; max-width:76ch;}
  .lede{font-size:16px; color:var(--pgmut);}
  code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9em;
       background:var(--pgsoft); padding:1px 5px; border-radius:4px;}
  .tag{display:inline-block; font-size:11px; font-weight:700; letter-spacing:.09em;
       text-transform:uppercase; padding:3px 8px; border-radius:4px; vertical-align:2px;}
  .tag.prop{background:#1A1A1A; color:#FFFFFF;}
  .tag.in{background:#E8F3EC; color:#1F5C38; border:1px solid #BEDCC9;}
  .tag.out{background:#F0F0F0; color:#555555; border:1px solid #DDDDDD;}
  .tag.ask{background:#FFF0E6; color:#8A4B10; border:1px solid #E8C6A8;}
  .tag.dep{background:#EEF2F7; color:#3B5570; border:1px solid #C9D6E4;}
  table{border-collapse:collapse; width:100%; margin:14px 0 8px; font-size:14px;}
  th,td{text-align:left; padding:9px 10px; border-bottom:1px solid var(--pgline); vertical-align:top;}
  th{font-size:11px; text-transform:uppercase; letter-spacing:.07em; color:var(--pgmut); font-weight:700;}
  td.num{text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap;}
  .note{border-left:3px solid var(--pgline); padding:2px 0 2px 14px; color:var(--pgmut);
        font-size:14px; margin:14px 0; max-width:76ch;}
  .warn{border-left-color:#C25A18; color:#7A3A0E;}
  .card{border:1px solid var(--pgline); border-radius:10px; background:#FFF; padding:20px 22px;
        margin:16px 0;}
  .card h3{margin-top:0; color:var(--pgink); font-size:17px; text-transform:none;
           letter-spacing:-.01em;}
  .card .plain{font-size:15.5px; max-width:70ch; margin:6px 0 12px;}
  .metrics{display:flex; flex-wrap:wrap; gap:22px; margin:10px 0 4px; font-size:13px;
           color:var(--pgmut);}
  .metrics b{display:block; font-size:19px; color:var(--pgink); font-variant-numeric:tabular-nums;
             letter-spacing:-.01em;}
  details{margin:10px 0 0;}
  summary{cursor:pointer; font-size:13px; color:var(--pgmut); padding:6px 0;}
  .paths{max-height:280px; overflow:auto; background:var(--pgsoft); border-radius:6px;
         padding:10px 12px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
         font-size:11.5px; line-height:1.7; color:#3A3A3A;}
  .q{border:1px solid #E8C6A8; background:#FFFCF8;}
  .q h3{color:#7A3A0E;}
  .opts{margin:14px 0 0; padding:0; list-style:none;}
  .opts li{margin:0 0 8px; padding:10px 12px; border:1px solid var(--pgline); border-radius:8px;
           background:#FFF; font-size:14.5px;}
  .opts label{display:flex; gap:10px; align-items:flex-start; cursor:pointer;}
  .rec{font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
       color:#1F5C38; margin-left:6px;}
  .head{display:flex; flex-wrap:wrap; gap:34px; padding:18px 22px; border:1px solid var(--pgline);
        border-radius:10px; background:var(--pgsoft); margin:18px 0 8px;}
  .head div b{display:block; font-size:24px; letter-spacing:-.02em;
              font-variant-numeric:tabular-nums;}
  .head div span{font-size:12px; color:var(--pgmut); text-transform:uppercase; letter-spacing:.07em;}
  ul{max-width:76ch;} li{margin:5px 0;}
  /* ⚠ MEASURED at 480px: the exclusions table forced the whole document to 798px wide, so the
     PAGE scrolled sideways rather than the table. Wide content scrolls inside its own box. */
  .tw{overflow-x:auto;}
  .tw>table{min-width:520px;}
"""


def render_page(man, zip_bytes=None, zip_sha=None, man_sha=None):
    G = {}
    for g in man["groups"]:
        G.setdefault(g["group"], []).append(g)
    gates = [g for g in man["groups"] if g["key"] == "gates"][0]
    c = gates["counts"]

    GROUP_LEAD = {
        "engine-canon": (
            "The engine itself",
            "This is the part you actually work in every day. Tokens, the contract for every "
            "component, the reference markup, the canon stylesheets, the compliance map, the "
            "real icons and the written guidelines. Nothing here is a summary of Apollo — it "
            "is Apollo."),
        "gates": (
            "The gates",
            "The checks that make Apollo a system rather than a folder of files. Every gate "
            "below was actually RUN inside a copy of this pack, on its own, outside your repo. "
            "The verdicts are measurements, not opinions — and the ones that only work here "
            "are named, with the reason, and left out."),
        "runbooks": (
            "The runbooks",
            "The written procedures. How to compose from canon. How to take a component "
            "through its gates. How to render a page and actually look at it. How to write a "
            "criteria contract before you build. How to bring an existing code library in."),
        "library": (
            "The library",
            "The showroom, alive — every component page, the foundations pages, the thumbnails, "
            "the index. Plus the rails file the library, the editor and the generator all read, "
            "and the render script so a designer can see their own work the way you do."),
        "memento-clean-cut": (
            "A clean cut of Memento",
            "The machinery only. The chain generator, retrieval, the graph edges, the gauge "
            "shim, the lexicon — and no record of any kind. No chain, no rulings, no state. "
            "Every project that adopts it grows its own memory from nothing, which is the "
            "point."),
        "skills": (
            "The skills",
            "Five, and they are written. Four rewritten against this knowledge base — the "
            "library is 135 components now, not 40, and the red law they quoted was three "
            "rulings out of date. The fifth is new: the gate-runner that actually runs the "
            "packed gates on a designer's own work, and reads the verdicts back honestly."),
    }

    out = []
    A = out.append
    A('<!doctype html>\n<meta charset="utf-8">')
    A('<title>Designer pack v3 — the release manifest — PROPOSED</title>')
    A('<!-- reviews/RELEASE-V3-MANIFEST-2026-08-26-v1.html — #219 R1.\n'
      '     GENERATED by knowledge/_release/_gen_v3_manifest.py --page. Do not hand-edit:\n'
      '     every count on this page is read out of _v3_manifest.json, which is itself\n'
      '     generated from a named commit. Nothing on this page is typed. -->')
    A('<link rel="stylesheet" href="../knowledge/canon/canon.css">')
    A('<link rel="stylesheet" href="../knowledge/canon/type.css">')
    A('<style>%s</style>' % PAGE_CSS)
    A('<div class="wrap">')

    A('<h1>Designer pack v3 — what ships <span class="tag prop">Proposed</span></h1>')
    A('<p class="lede">#219 lane R1 · 2026-08-26 · nothing is baked, nothing is committed, '
      'no release exists. This page is the list, for your eye. The bake does not run until '
      'you say it does.</p>')

    A('<h2>The short version</h2>')
    A('<p>You said you wanted designers to get <em>as close to what you use as possible, '
      'without the review files and the extras, even a clean cut of Memento</em>. This is that '
      'list. It is six groups. Five of them are things you already work in; the sixth is '
      'Memento with its memory emptied out.</p>')
    A('<p>The list is not typed by hand. It is worked out from one named commit, so the pack '
      'and the repo can never quietly disagree — and building the same commit twice gives a '
      'file that is <b>identical down to the byte</b>, which is what makes it possible to see '
      'exactly what changed between two releases.</p>')

    A('<div class="head">')
    A('<div><b>%s</b><span>files in the pack</span></div>' % "{:,}".format(man["totals"]["files"]))
    A('<div><b>%s</b><span>on disk</span></div>' % mb(man["totals"]["bytes"]))
    if zip_bytes:
        A('<div><b>%s</b><span>zipped — the download</span></div>' % mb(zip_bytes))
    A('<div><b>%d</b><span>gates that run anywhere</span></div>' % (c["runnable"] + c["needs_dep"]))
    A('<div><b>%d</b><span>questions for you</span></div>' % len(man["open_questions"]))
    A('</div>')
    A('<p class="note">Read from commit <code>%s</code> (%s) — nothing has been baked. '
      'Manifest fingerprint '
      '<code>%s</code>. Version <code>%s</code>.</p>'
      % (esc(man["commit"][:12]), esc(man["commit_date"][:10]),
         esc((man_sha or "")[:16]), esc(man["version"])))

    # ---- the groups, one card each
    A('<h2>What goes in — one card per group</h2>')
    for gk in ["engine-canon", "gates", "runbooks", "library", "memento-clean-cut", "skills"]:
        entries = G.get(gk, [])
        if not entries:
            continue
        t = man["totals"]["by_group"][gk]
        lead_title, lead_plain = GROUP_LEAD[gk]
        A('<div class="card">')
        A('<h3>%s <span class="tag in">In</span></h3>' % esc(lead_title))
        A('<p class="plain">%s</p>' % esc(lead_plain))
        A('<div class="metrics"><div><b>%s</b>%s</div><div><b>%s</b>on disk</div></div>'
          % ("{:,}".format(t["files"]), "files in this group", mb(t["bytes"])))
        A('<table><tr><th>part</th><th>what it is</th><th class="num">files</th>'
          '<th class="num">size</th></tr>')
        for e in entries:
            A('<tr><td><b>%s</b></td><td>%s</td><td class="num">%s</td><td class="num">%s</td></tr>'
              % (esc(e["title"]), esc(e["plain"]), "{:,}".format(e["files"]), mb(e["bytes"])))
        A('</table>')

        if gk == "gates":
            A(render_gate_table(gates))
            # #219 R2 — the pack-side half of "CI both halves". Rendered only when the files
            # are actually in the commit the manifest was built from, so this page can never
            # promise a designer a workflow that is not in the zip.
            if gates.get("ci_template"):
                A('<p class="note"><b>The pack ships a CI workflow too.</b> %d file(s) under '
                  '<code>designer-skills-v3/ci-template/</code>: a GitHub Actions workflow a '
                  'designer copies into their own repo, the runner it calls, and a README that '
                  'says what blocks, what only advises, and how to turn a check off honestly '
                  '(delete the step — never hide it behind continue-on-error).</p>'
                  % len(gates["ci_template"]))
        # #219 seam 7: the "Empty slot, named" renderer is GONE with its producer. Leaving the
        # consumer behind was not harmless — rendered against a manifest generated before the
        # repoint it still painted "PLACEHOLDER — R3 writes it" onto Dave's page for a skill
        # that exists (measured, not reasoned: it fired on the stale manifest during this seam).
        # A consumer that outlives its producer keeps telling the old story to whoever feeds it
        # old data. [[instrument-without-a-consumer]], inverted.

        allp = sorted({p for e in entries for p in e["paths"]})
        A('<details><summary>Every path in this group (%s)</summary><div class="paths">%s</div>'
          '</details>' % ("{:,}".format(len(allp)), "<br>".join(esc(p) for p in allp)))
        A('</div>')

    # ---- what stays out
    A('<h2>What stays out, and why <span class="tag out">Out</span></h2>')
    A('<p>Every line below is a deliberate exclusion, not an oversight. Three reasons cover '
      'nearly all of it: it is your working paperwork, it is your session record, or we do not '
      'hold a licence that lets us pass it on.</p>')
    A('<table><tr><th>what</th><th>why it stays here</th></tr>')
    for x in man["excluded"]:
        A('<tr><td><code>%s</code></td><td>%s</td></tr>' % (esc(x["path"]), esc(x["reason"])))
    A('</table>')

    # ---- the open questions
    # #219 seam 7: the count was the word "Four", typed, while the list beside it was data. A
    # fifth card would have left the heading lying on Dave's own decision surface, which is the
    # [[banner-figures-are-parsed-not-prose]] class one inch from where he rules. Now derived.
    _NW = {1: "One thing", 2: "Two things", 3: "Three things", 4: "Four things",
           5: "Five things", 6: "Six things", 7: "Seven things"}
    _nq = len(man["open_questions"])
    A('<h2>%s only you can settle <span class="tag ask">Ask</span></h2>'
      % _NW.get(_nq, "%d things" % _nq))
    A('<p>None of these are blocked on work. They are all judgement calls about where a line '
      'sits. Nothing is pre-selected.</p>')
    for q in man["open_questions"]:
        A('<div class="card q">')
        A('<h3>%s. %s</h3>' % (esc(q["id"]), esc(q["title"])))
        # Short paragraphs, not a wall. The body carries `||` where a break belongs — Dave
        # reads one idea per block, and an unbroken twelve-line paragraph is the format he
        # has already told us costs him time.
        for para in q["body"].split("||"):
            A('<p class="plain">%s</p>' % esc(para.strip()))
        A('<ul class="opts">')
        for i, o in enumerate(q["options"]):
            rec = " recommended" in o or "(recommended" in o
            A('<li><label><input type="radio" name="%s" value="%d"><span>%s%s</span></label></li>'
              % (esc(q["id"]), i, esc(o.replace(" (recommended)", "").replace(" — recommended", "")),
                 '<span class="rec">recommended</span>' if rec else ""))
        A('</ul></div>')

    # ---- how the bake works
    A('<h2>How it gets built, once you say yes</h2>')
    A('<p>One command, from a commit you name. It refuses to run on a messy working tree, it '
      'refuses to run without a commit, and it refuses to cut a release at all while this page '
      'still says <em>Proposed</em>. That last refusal is the one that matters: the release is '
      'your word, not the script\'s.</p>')
    A('<details><summary>The commands</summary><div class="paths">'
      'bash designer-skills-v3/build-designer-pack.sh --manifest --commit &lt;sha&gt;<br>'
      'bash designer-skills-v3/build-designer-pack.sh --dry-run --out-dir /var/tmp/x '
      '--commit &lt;sha&gt;<br>'
      'bash designer-skills-v3/build-designer-pack.sh --release --commit &lt;sha&gt;<br>'
      'bash designer-skills-v3/build-designer-pack.sh --check &lt;zip&gt; --commit &lt;sha&gt;'
      '</div></details>')
    if zip_sha:
        A('<p class="note">Proved today on a throwaway copy: built twice, into two different '
          'directories, and both files came out with the same fingerprint '
          '<code>%s</code>. Then checked back against the commit, file by file — green; '
          'and with one byte changed in one token file — red, naming the file.</p>'
          % esc(zip_sha[:16]))

    A('<p class="note warn"><b>Nothing here is enacted.</b> <code>designer-skills-v3/</code> '
      'holds the build script and nothing else. No pack has been baked, no zip exists in '
      '<code>dist/</code>, and no ruling was written. v1 and v2 are untouched.</p>')
    A('</div>')
    html = "\n".join(out) + "\n"
    # Every table gets a scroll box. Done here rather than at each emit site so a table added
    # later cannot forget it — the responsive rule is enforced once, not remembered three times.
    html = html.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return html


def render_gate_table(gates):
    rows = ['<h3 style="text-transform:none;letter-spacing:0;color:#1A1A1A;font-size:15px;'
            'margin-top:22px">Every gate, and whether it works away from home</h3>',
            '<p style="font-size:14.5px;max-width:70ch">Each one was copied into a bare '
            'directory holding only the pack, and run. Three answers: it works; it works but '
            'needs something installed first; or it only makes sense inside your repo, in '
            'which case it stays here and the reason is written down.</p>',
            '<table><tr><th>gate</th><th>verdict</th><th>what happened when it ran</th>'
            '<th>own tests</th></tr>']
    order = {"RUNNABLE": 0, "NEEDS-DEP": 1, "REPO-BOUND": 2}
    for v in sorted(gates["verdicts"], key=lambda r: (order[r["verdict"]], r["gate"])):
        tag = {"RUNNABLE": "in", "NEEDS-DEP": "dep", "REPO-BOUND": "out"}[v["verdict"]]
        label = v["verdict"]
        if v["verdict"] == "NEEDS-DEP":
            label = "needs " + esc(v["why"])
        extra = ""
        if v.get("population") == "EMPTY-IN-PACK":
            extra = (' <span class="tag ask">nothing to grade yet</span>')
        st = {"green": "pass", "red": "fail", "crashed": "won’t run here",
              "none": "none"}.get(v["selftest"], v["selftest"])
        rows.append('<tr><td><code>%s</code></td><td><span class="tag %s">%s</span>%s</td>'
                    '<td>%s</td><td>%s</td></tr>'
                    % (esc(v["gate"]), tag, esc(label), extra, esc(v["why"]), esc(st)))
    rows.append('</table>')
    rows.append('<p class="note">Three gates want <code>playwright</code> installed because '
                'they drive a real browser. They ship anyway and say so themselves when you '
                'run them without it. The ones marked <em>nothing to grade yet</em> run '
                'perfectly — they simply have no work of the designer’s to look at until '
                'the designer makes some.</p>')
    return "\n".join(rows)


# ---------------------------------------------------------------------------------------------
# THE ZIP — deterministic by construction
# ---------------------------------------------------------------------------------------------

def deterministic_zip(stage, out_zip, epoch, prefix=None):
    """Fixed mtimes (the COMMIT's), sorted order, fixed external attrs, no extra fields.
    Two runs over the same stage produce byte-identical archives.

    `prefix` wraps everything in ONE root folder — both so unzipping does not spray files into
    the user's cwd, and because --check's fidelity test needs a single root to strip."""
    import time
    dt = time.gmtime(epoch)
    date_time = (dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec)
    files = []
    for dirpath, dirnames, filenames in os.walk(stage):
        dirnames.sort()
        for f in sorted(filenames):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, stage)
            files.append((prefix + "/" + rel if prefix else rel, full))
    files.sort(key=lambda t: t[0])
    os.makedirs(os.path.dirname(os.path.abspath(out_zip)), exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel, full in files:
            zi = zipfile.ZipInfo(rel, date_time=date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o644 << 16)
            zi.create_system = 3
            with open(full, "rb") as fh:
                z.writestr(zi, fh.read(), compresslevel=9)
    return out_zip


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------------------------
# --check — a baked pack against manifest + commit
# ---------------------------------------------------------------------------------------------

def check_pack(zip_path, man, sha):
    fails = []
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        want = set(all_paths(man))
        # the pack root is <pack>/<repo path>; strip the single root component
        roots = {n.split("/")[0] for n in names}
        if len(roots) != 1:
            fails.append("pack has %d roots, expected 1: %s" % (len(roots), sorted(roots)[:5]))
        root = sorted(roots)[0] if roots else ""
        # ⚠ THE ROOT README, addressed exactly. The first cut picked it with a substring match
        # over a SET, which also matched `knowledge/README.md` — and set iteration order is
        # hash-randomised per process, so the same zip checked twice gave different answers.
        # A non-deterministic check is worse than no check.
        readme = [n for n in names if n == root + "/README.md"]
        got = {n[len(root) + 1:] for n in names if n.startswith(root + "/")}
        generated = {p for p in got if p in ("README.md", "PROVENANCE.json", "_MANIFEST.json")}
        missing = sorted(want - got)
        extra = sorted(got - want - generated)
        if missing:
            fails.append("%d manifest path(s) MISSING from the pack, first: %s"
                         % (len(missing), missing[:5]))
        if extra:
            fails.append("%d path(s) in the pack that the manifest does not name, first: %s"
                         % (len(extra), extra[:5]))
        # byte fidelity against the commit
        want_sha = blob_shas(sha, sorted(want & got))
        bad = []
        for p in sorted(want & got):
            data = z.read(root + "/" + p)
            oid = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
            if want_sha.get(p) and oid != want_sha[p]:
                bad.append(p)
        if bad:
            fails.append("%d file(s) differ from the commit's blobs, first: %s"
                         % (len(bad), bad[:5]))
        if readme:
            txt = z.read(readme[0]).decode("utf8", "replace")
            if sha not in txt:
                fails.append("pack README does not carry the commit sha %s" % sha[:12])
            if manifest_hash(canonical(man)) not in txt:
                fails.append("pack README does not carry the manifest hash")
        else:
            fails.append("pack has no README.md at its root")
    return fails


# ---------------------------------------------------------------------------------------------
# selftest — mutation-tested both directions
# ---------------------------------------------------------------------------------------------

def selftest():
    fails = []
    n = [0]

    def bite(name, got, want, why=""):
        n[0] += 1
        if got != want:
            fails.append("[%s] got %r, wanted %r %s" % (name, got, want, why))

    # ---- classifier: the verdicts are a function of the RUN, and each arm can fail
    v, w = classify(0, "all green", "", set())
    bite("classify/clean-pass", v, "RUNNABLE")
    v, w = classify(1, "FAIL: 3 components missing a binding", "", set())
    bite("classify/clean-fail", v, "RUNNABLE", "a verdict is a run")
    v, w = classify(1, "", TRACE + "\nModuleNotFoundError: No module named 'playwright'", set())
    bite("classify/needs-dep", v, "NEEDS-DEP")
    bite("classify/needs-dep-name", w, "playwright")
    v, w = classify(1, "", TRACE + "\nFileNotFoundError: [Errno 2] No such file or directory: "
                                   "'/x/reviews/_REVIEW-QUEUE.json'", set())
    bite("classify/repo-bound", v, "REPO-BOUND")
    bite("classify/repo-bound-names-why", "reviews/_REVIEW-QUEUE.json" in w, True)
    v, w = classify(1, "", TRACE + "\nFileNotFoundError: [Errno 2] No such file or directory: "
                                   "'/x/knowledge/tokens/colour.json'",
                    {"knowledge/tokens/colour.json"})
    bite("classify/shipped-path-is-not-repo-bound", v, "RUNNABLE",
         "a path error INSIDE the shipped set is a verdict, not a fence")
    v, w = classify(124, "", "", set())
    bite("classify/timeout", v, "REPO-BOUND")

    # ---- the courteous-refusal arm: a gate that CATCHES ImportError and prints prose is still
    # a missing dependency. This is the bite that the narrow `ModuleNotFoundError:` regex failed.
    v, w = classify(77, "COULD-NOT-ASK: the 'playwright' module is not installed "
                        "(ModuleNotFoundError(\"No module named 'playwright'\"))", "", set())
    bite("classify/caught-import", v, "NEEDS-DEP")
    bite("classify/caught-import-name", w, "playwright")

    # ---- the SUBJECT test, both directions. A missing-language line naming an unshipped path
    # is REPO-BOUND; the very same path shape in a non-missing line must NOT trip it.
    v, w = classify(1, "UNPARSEABLE — GOOD-MORNING.md — file not found", "",
                    {"knowledge/tokens/colour.json"})
    bite("classify/subject-missing", v, "REPO-BOUND")
    v, w = classify(1, "glob      : knowledge/canon/*.css  (2 file(s))\n"
                       "parsed    : 12009 declarations\nFORK: --c-x forks --c-y", "",
                    {"knowledge/canon/canon.css"})
    bite("classify/subject-present-is-a-verdict", v, "RUNNABLE",
         "a path named in a line it successfully READ must not read as a fence")
    v, w = classify(1, "✗ VERBATIM SET: source knowledge/_gen_chain.py does not exist", "",
                    {"knowledge/canon/canon.css"})
    bite("classify/subject-named-in-why", "_gen_chain.py" in w, True)

    # ---- the vacuous-pass detector, both directions. This is the bite the first cut failed.
    bite("empty-pop/zero-inputs",
         bool(EMPTY_POP.search("✅ No-hardcode gate passed (0 tranche file(s)).")), True)
    bite("empty-pop/zero-failures-is-NOT-empty",
         bool(EMPTY_POP.search("a11y gate: 135 snippet(s), 0 failure(s), 286 warning(s)")), False,
         "zero FAILURES is the good news; only zero FILES is an empty subject")
    bite("empty-pop/zero-warnings-is-NOT-empty",
         bool(EMPTY_POP.search("gate: 40 page(s), 0 warning(s)")), False)

    # ---- path naming: the probe's stage prefix must never reach Dave's page
    bite("tail/strips-stage",
         _tail("/var/tmp/v3probe-abc/pack/knowledge/_state.json"), "knowledge/_state.json")
    bite("tail/keeps-plain-path", _tail("knowledge/canon/canon.css"), "knowledge/canon/canon.css")

    # ---- the args-refusal arm
    v, w = classify(2, "✖ HIT-AREA: no input files. Pass paths or --all.", "", set())
    bite("classify/args-refusal", v, "RUNNABLE")

    # ---- MUTATION: a classifier that answered from the source rather than the run would call
    # a playwright import REPO-BOUND. Prove the discriminator is the message, not the exit code.
    v1, _ = classify(1, "", TRACE + "\nModuleNotFoundError: No module named 'playwright'", set())
    v2, _ = classify(1, "", TRACE + "\nFileNotFoundError: 'runs/x.json'", set())
    bite("classify/discriminates", v1 != v2, True)

    # ---- the group table: no path may be claimed twice, and every group must be reachable
    tbl = groups()
    keys = [g["key"] for g in tbl]
    bite("groups/unique-keys", len(keys), len(set(keys)))
    probe_paths = ["knowledge/tokens/colour.json", "knowledge/components/button.meta.json",
                   "knowledge/snippets/button.reference.html", "knowledge/canon/canon.css",
                   "knowledge/_validate_radius.py", "showroom/index.json",
                   "memento-package/machinery/_gen_chain.py",
                   "designer-skills-v3/skills/generate-from-canon/SKILL.md",
                   "designer-skills-v3/skills/check-with-gates/SKILL.md",
                   "knowledge/_RUNBOOK-compose-from-canon.md"]
    for p in probe_paths:
        hits = [g["key"] for g in tbl if g["match"](p)]
        bite("groups/claims:%s" % os.path.basename(p), len(hits) >= 1, True,
             "no group claims it")
    # excluded paths must be claimed by NOBODY
    for p in ["reviews/x.html", "notes/_briefs/x.md", "knowledge/tokens/_raw/x.json",
              "API-KEY.txt", "GOOD-MORNING.md", "knowledge/_rulings.json",
              "knowledge/assets/photography-web/x.jpg", "designer-skills-v1/knowledge/x.json",
              "knowledge/_RUNBOOK-capture-ritual.md", "knowledge/_state.json",
              # #219 seam 7, the repoint proved in the OTHER direction: v2 is a FROZEN release
              # (s114-D4) and its SKILL.md must now be claimed by nobody. Without this bite the
              # skills match could silently widen back to v2 and only the ship list would know.
              "designer-skills-v2/generate-from-canon/SKILL.md"]:
        hits = [g["key"] for g in tbl if g["match"](p)]
        bite("groups/excludes:%s" % p, hits, [], "an EXCLUDED path was claimed by %s" % hits)

    # ---- the open questions (#219 seam 7). Dave's decision surface is generated from this list,
    # so the list is what has to be checked — the page cannot be trusted to police itself.
    qids = [q["id"] for q in OPEN_QUESTIONS]
    bite("questions/unique-ids", len(qids), len(set(qids)))
    for q in OPEN_QUESTIONS:
        bite("questions/has-body:%s" % q["id"], len(q["body"].strip()) > 40, True)
        bite("questions/two-or-more-options:%s" % q["id"], len(q["options"]) >= 2, True,
             "a question with one answer is not a question")
    q5 = [q for q in OPEN_QUESTIONS if q["id"] == "Q5"]
    bite("questions/Q5-present", len(q5), 1, "R2's Q1 card — four gates arrive red at bake")
    if q5:
        body = q5[0]["body"]
        # Named, and STILL REAL. A card naming a renamed gate lies quietly on Dave's own page.
        for gname in Q5_RED_GATES:
            bite("questions/Q5-names:%s" % gname, gname in body, True,
                 "the red-gate card must state the gate by name")
            bite("questions/Q5-gate-exists:%s" % gname,
                 os.path.exists(os.path.join(ROOT, "knowledge", gname)), True,
                 "the card names a gate that is no longer in the repo — re-derive it")
        bite("questions/Q5-three-dispositions", len(q5[0]["options"]), 3,
             "fix-before-bake / baseline / ship-red-documented")
        # It is a QUESTION card. The renderer paints a 'recommended' flag on any option whose
        # text carries the word, and this one must not carry it in any option: seam 7 was told
        # to put the choice to Dave, not to make it. [[dont-launder-a-premise-into-a-ruling]]
        bite("questions/Q5-decides-nothing",
             [o for o in q5[0]["options"] if "recommended" in o], [],
             "the red-gate card must not pre-select a disposition")

    # ---- determinism: canonical() is order-independent
    a = canonical({"b": 1, "a": [3, 2]})
    b = canonical({"a": [3, 2], "b": 1})
    bite("canonical/stable", a, b)
    bite("canonical/mutation", canonical({"a": [2, 3], "b": 1}) != a, True,
         "a real content change MUST change the bytes")

    # ---- deterministic_zip: same stage twice ⇒ identical bytes; a content change ⇒ different
    tmp = tempfile.mkdtemp(prefix="v3ziptest-", dir="/var/tmp")
    try:
        st = os.path.join(tmp, "stage")
        os.makedirs(os.path.join(st, "sub"))
        open(os.path.join(st, "a.txt"), "w").write("alpha\n")
        open(os.path.join(st, "sub", "b.txt"), "w").write("beta\n")
        z1 = deterministic_zip(st, os.path.join(tmp, "1.zip"), 1700000000, prefix="pack")
        os.utime(os.path.join(st, "a.txt"), (0, 0))          # mtime noise MUST NOT matter
        z2 = deterministic_zip(st, os.path.join(tmp, "2.zip"), 1700000000, prefix="pack")
        bite("zip/reproducible", sha256_file(z1), sha256_file(z2))
        with zipfile.ZipFile(z1) as _z:
            bite("zip/single-root", sorted({n.split("/")[0] for n in _z.namelist()}), ["pack"])
        open(os.path.join(st, "a.txt"), "w").write("alphaX\n")
        z3 = deterministic_zip(st, os.path.join(tmp, "3.zip"), 1700000000, prefix="pack")
        bite("zip/mutation", sha256_file(z3) != sha256_file(z1), True,
             "a content change MUST change the zip — otherwise the check is vacuous")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("selftest: %d bites, %d fail(s)" % (n[0], len(fails)))
    for f in fails:
        print("  RED " + f)
    return not fails


# ---------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--stage")
    ap.add_argument("--zip")
    ap.add_argument("--check")
    ap.add_argument("--page", help="write Dave's go/no-go page to this path")
    ap.add_argument("--zip-bytes", type=int, help="--page: the proved zip size, in bytes")
    ap.add_argument("--zip-sha", help="--page: the proved zip fingerprint")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--commit")
    ap.add_argument("--out")
    ap.add_argument("--only", help="probe only these gate basenames (comma separated)")
    ap.add_argument("--probe-stage", help="reuse an existing probe stage dir")
    ap.add_argument("--full-stage", help="a git-archive stage of the WHOLE commit, for the "
                                         "differential arm (never the repo itself)")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(0 if selftest() else 1)

    if a.probe:
        if not a.commit:
            print("REFUSED: --probe needs --commit <sha> (a probe of 'the tree' is a probe of "
                  "nothing reproducible)", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        if a.full_stage and os.path.abspath(a.full_stage) == ROOT:
            print("REFUSED: --full-stage may not be the repo itself — a validator that writes "
                  "an audit file would dirty the tree (#158 write-by-default class).",
                  file=sys.stderr)
            sys.exit(2)
        probe, tmp = probe_gates(sha, stage_root=a.probe_stage, verbose=a.verbose,
                                 full_stage=a.full_stage,
                                 only=set(a.only.split(",")) if a.only else None)
        out = a.out or PROBE_PATH
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(canonical(probe))
        print("probe -> %s (stage %s)" % (out, tmp))
        return

    if a.manifest:
        if not a.commit:
            print("REFUSED: --manifest needs --commit <sha>", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        if not os.path.exists(PROBE_PATH):
            print("REFUSED: no gate probe at %s — run --probe first. The gate verdicts are "
                  "MEASURED; a manifest that guessed them would be prose." % PROBE_PATH,
                  file=sys.stderr)
            sys.exit(2)
        probe = json.load(open(PROBE_PATH))
        if probe["commit"] != sha:
            print("REFUSED: the gate probe was run at %s, not %s. Re-probe."
                  % (probe["commit"][:12], sha[:12]), file=sys.stderr)
            sys.exit(2)
        man = build_manifest(sha, probe)
        # The totals must be the count of DISTINCT shipped paths. A group table that let a path
        # be owned twice would inflate the size on Dave's go/no-go page — the number he is
        # ruling on has to be the number the bake produces.
        if len(all_paths(man)) != man["totals"]["files"]:
            print("REFUSED: totals say %d files but the distinct path set is %d — a path is "
                  "owned by two groups." % (man["totals"]["files"], len(all_paths(man))),
                  file=sys.stderr)
            sys.exit(2)
        text = canonical(man)
        out = a.out or MANIFEST_PATH
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(text)
        print("manifest -> %s" % out)
        print("  commit %s  files %d  bytes %d  sha256 %s"
              % (sha[:12], man["totals"]["files"], man["totals"]["bytes"],
                 manifest_hash(text)[:16]))
        return

    if a.page:
        text = open(MANIFEST_PATH).read()
        man = json.loads(text)
        html = render_page(man, zip_bytes=a.zip_bytes, zip_sha=a.zip_sha,
                           man_sha=manifest_hash(text))
        os.makedirs(os.path.dirname(os.path.abspath(a.page)), exist_ok=True)
        open(a.page, "w").write(html)
        print("page -> %s (%d bytes)" % (a.page, len(html)))
        return

    if a.stage:
        if not a.commit:
            print("REFUSED: --stage needs --commit <sha>", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        man = json.load(open(a.out or MANIFEST_PATH))
        if man["commit"] != sha:
            print("REFUSED: manifest is for %s, you asked for %s"
                  % (man["commit"][:12], sha[:12]), file=sys.stderr)
            sys.exit(2)
        extract(sha, all_paths(man), a.stage)
        print("staged %d paths -> %s" % (len(all_paths(man)), a.stage))
        return

    if a.zip:
        if not a.commit or not a.out:
            print("REFUSED: --zip needs --commit and --out", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        deterministic_zip(a.zip, a.out, commit_epoch(sha),
                          prefix=os.path.basename(os.path.normpath(a.zip)))
        print("%s  %s" % (sha256_file(a.out), a.out))
        return

    if a.check:
        if not a.commit:
            print("REFUSED: --check needs --commit <sha>", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        man = json.load(open(MANIFEST_PATH))
        fails = check_pack(a.check, man, sha)
        if fails:
            print("CHECK RED — %d problem(s):" % len(fails))
            for f in fails:
                print("  " + f)
            sys.exit(1)
        print("CHECK GREEN — %s matches the manifest at %s" % (a.check, sha[:12]))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
