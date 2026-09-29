#!/usr/bin/env python3
"""_validate_evidence.py — the evidence linter for claim/challenge JSONL (W-44, `s204-D1` leg 3).

TWO LEGS, both ruled in `s204-D1`.

LEG 1 — `s182-D1` CONFORMANCE. Every MECHANICAL row must carry its PROBEABLE TOKEN: something
a reader can RE-RUN or RE-READ. Three token shapes count:
  · COMMAND — a backticked shell command whose head verb is a real tool (`python3 … --check`,
    `git ls-files …`, `grep -c …`, `sed -n '299p' …`)
  · PATH    — a repo-relative path that EXISTS on disk, optionally `:line`
  · FIGURE  — `rc=N`, or a number carrying a unit/keyword (`1097 violation(s)`, `91 snippet(s)`)
A row is MECHANICAL when tag ∈ {PROVEN, MEASURED} or verdict ∈ {CONFIRMED, CONTRADICTED, NEW}.
Rows tagged CLAIMED/UNPROVEN and verdict UNTESTED are EXEMPT — they assert no first-hand
mechanism, and forcing a token onto them would manufacture false provenance.
⛔ A PATH token that does NOT EXIST is a HARD FAIL: a dead pointer is worse than no pointer,
because it reads as evidence (`ritual-output-is-not-evidence`).

⛔ #208 — THREE POINTER DIALECTS, because the rule above had no legal form for two honest
statements and one laundering hole (all three found by driving the #208 verifier wave):
  · `absent:knowledge/_foo.py` — an ABSENCE CLAIM. The linter checks the path does NOT exist,
    and HARD-FAILS if it does. Before this, a finding whose whole subject was a missing file
    had to HIDE the path behind an `rc=1, no output` figure — the linter was satisfied by
    hiding the subject (`honest-refusal-needs-a-legal-form`, three independent instances).
  · `notes/_vfy.txt (NON-REPO: /…/vfy/full)` — the RULED `s191-D2` marker, now HONOURED. A
    verifier's material genuinely lives in scratch clones; the marker declares WHERE and the
    existence check stands down for that pointer only (marker must follow within 60 chars).
  · `notes/_vfy.txt…` — a trailing ellipsis USED TO PASS UNCHECKED, so one keystroke laundered
    any dead pointer past the gate. It is now resolved as a PREFIX: at least one real path must
    start with it, else it is a DEAD POINTER like any other. `*`/`?`/`[` globs are unchanged.

LEG 2 — SAMPLING. A seeded random subset of rows has its first COMMAND token RE-RUN and its
exit code compared with the row's declared `rc`. `--seed` makes every run reproducible; the
seed and the drawn ids are PRINTED, so a report can quote which rows were actually sampled.

⛔ #208 — AN EXIT CODE IS NOT AN OBSERVATION. `git show`, `grep -c`, `find`, `ls` and `sed -n`
exit 0 for ANY content, so for read-style evidence — most of a claim table — rc-only sampling
proves RUNNABILITY, not REPRODUCTION. The #208 verifier watched this gate print PASS over two
rows whose content it had just proved false. A row may now declare `expect_stdout_contains`
(substring of stdout) and/or `expect_count` (the last stdout line, as an integer); when either
is present the sampler compares the OBSERVATION and an OBSERVATION MISMATCH is a rc=1 failure.
Rows without them behave EXACTLY as before — the schema changed by ADDITION.

⛔ THE REFUSAL CONTRACT (the reason this linter does not lie): a command it cannot honestly run
is REFUSED — loudly, by name, with the reason — and never defaulted to a pass. Three refusal
classes, all counted separately from passes:
  · SIDE-EFFECTS — e.g. a bare `python3 knowledge/_validate_*.py`, which REWRITES a tracked
    audit file. #204 declared this stop twice (`_validate_state_contrast.py`); a linter that
    "verified" evidence by dirtying the tree would be a worse instrument than none.
  · UNSAFE-TO-JUDGE — `python3 -c …`, `bash …`, redirects, `rm`/`mv`/`git checkout`: arbitrary
    effect, no allowlist can vouch for it.
  · NOT-IN-THIS-ENVIRONMENT — head verb absent from PATH. A DECLARED environment gap, per
    `feedback-measuring-tool-must-not-guess`: UNKNOWN is never defaulted.
Refusals make the linter print a DECLARED GAP block. They do not fake a green: `--strict-sample`
turns any refusal into rc=1 for a caller that needs every sampled row actually run.

⛔ #308 — JUDGE AT THE COMMIT, READ WHAT THE ROW MEANT, DECLARE WHAT CANNOT BE PROBED (s308-D29).
Dave, 2026-09-29 13:09, choosing (a) and (b) together over the recommended (b) alone: "Lets do
this properly, I'd rather rebuild than patch". Lane C measured the nine red rows: two had gone
stale, three were the checker MISREADING true rows, three were never probeable, one was CI-only.
  · AT THE COMMIT — each row is judged in the tree of the commit that WROTE it (`git blame
    --porcelain`, per line). Pointers resolve in `git ls-tree <sha>`; a sampled command is re-run
    in a throwaway `--shared` clone checked out at that commit, outside the repo (see `History`
    for why not `git worktree add` on the mount). An uncommitted row is judged in the working
    tree. A SHALLOW checkout is COULD-NOT-ASK (77) for the whole gate. `--at-head` restores the
    pre-#308 reading, for comparison.
  · ENVIRONMENT IS COULD-NOT-ASK, NEVER A MISMATCH — rc=77 from the command, rc=126/127, a missing
    third-party module, a timeout, a head verb not on PATH (`env_failure`). Counted apart.
  · A PATH QUOTED FROM A TOOL'S OUTPUT resolves against that tool's base (its directory and
    ancestors), after the repo root fails — `output_tool`, `tool_bases`.
  · AN ABSENCE STATED IN WORDS ("`x`, a path that does not exist") is judged as an absence.
  · DECLARED NOTES — a token-less mechanical row is excused ONLY by a dated note in the sidecar
    `notes/_claims/_declared-notes.jsonl`, addressed by table + line + id + kind, citing a ruling.
    It is counted and printed as DECLARED, never a pass; it cannot excuse a dead pointer or a
    mismatch; a note whose address does not resolve is a hard fail (`load_notes`).
Still ADVISORY in CI: making it blocking is Dave's call, and it is not ruled here.

USAGE
  python3 knowledge/_validate_evidence.py <rows.jsonl> [<rows2.jsonl> …]
                                          [--sample N] [--seed S] [--no-sample] [--strict-sample]
                                          [--at-head]
  python3 knowledge/_validate_evidence.py --selftest

EXIT: 0 clean · 1 lint failure, parse residual, rc mismatch (or a refusal under --strict-sample)
      · 2 bad invocation · 77 COULD-NOT-ASK (#219, see below).

⛔ #219 — A BARE INVOCATION IS LEGAL, AND HAS THREE HONEST ANSWERS. This gate used to exit 2
with no argument, which is *bad arguments* and not a verdict at all — so the gate shipped in the
Apollo pack could NEVER pass however it was called, and it was the first of the four packed-gate
reds `s219-D5(Q5)` sent back to be fixed AT CAUSE. Bare now defaults to `notes/_claims`, the
same path the two wired invocations name, so a workflow line and this gate cannot drift apart.
When that home is absent — the pack's case and a fresh designer project's case, because `notes/`
is deliberately outside the release ship list — the answer is **COULD-NOT-ASK (77)** with the
unreachable input NAMED (`_could_not_ask.py`), never a FAIL and never a silent pass. Naming a
table or a directory always overrides the default.

CONSUMER at birth: the PM-wave seam, alongside `_join_claim_tables.py`.
✅ WIRED #208 — the `s204-D1` precondition (driven in >= 1 real wave) was MET by the #208
verifier wave (55 claim rows, 60 challenges, receipt `notes/_receipts/2026-08-19-208-verifier-
wave.md`) and Dave ruled the wiring. Now `_build_all.STEPS` (ADVISORY) over `notes/_claims`,
plus its own CI step in the `gates` job. ADVISORY and not blocking BY MEASUREMENT: the frozen
#204/#206/#207 tables carry lint failures ADR-0017 does not let a later lane rewrite.
⬛ Promoting it to BLOCKING is DAVE'S.
A DIRECTORY argument is legal and lints every `*.jsonl` in it; relative paths resolve against
the repo root, so the step does not depend on the build's cwd.

Selftest: plants a token-less mechanical row, a dead path pointer, and an rc mismatch — each
must be named; removing each must go green. Includes a REFUSAL arm proving a side-effecting
command is refused rather than run, and a determinism arm proving the same seed draws the
same rows. #219 adds a NO-MATERIAL arm in BOTH directions, driven in a throwaway tree with cwd
and ROOT both moved: absent home -> 77, empty home -> 77, and a PLANTED bad row under a present
home -> 1, so the refusal is shown not to have swallowed the gate.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import sys, os, re, json, glob, random, shutil, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _claimtable as CT
import _could_not_ask as CNA          # #219 — the third verdict, for the no-material case

# #219 — the conventional home of this repo's claim tables. `_build_all.py` and the house
# workflow both name it explicitly; this constant is what a BARE invocation falls back to, so
# the three cannot drift apart. It is a PATH, not a policy: naming a table always wins.
DEFAULT_CLAIMS = os.path.join("notes", "_claims")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SEED = 205
DEFAULT_SAMPLE = 5

MECHANICAL_TAGS = ("PROVEN", "MEASURED")
MECHANICAL_VERDICTS = ("CONFIRMED", "CONTRADICTED", "NEW")

VERBS = ("python3", "python", "git", "grep", "rg", "ls", "sed", "awk", "wc", "cat", "head",
         "tail", "find", "jq", "node", "bash", "sh", "test", "diff", "stat", "file", "printf")
# Read-only heads the sampler may execute. Everything else is REFUSED, never guessed.
SAFE_VERBS = ("git", "grep", "rg", "ls", "sed", "awk", "wc", "cat", "head", "tail", "find",
              "jq", "test", "diff", "stat", "file", "printf", "echo")
UNSAFE_MARKERS = (">", ">>", "rm ", "mv ", "cp ", "checkout", "restore", "stash", "commit",
                  "push", "reset", "|& ", "$(", "`")
CMD_RE = re.compile(r"`([^`]+)`")
PATH_RE = re.compile(r"(?<![\w/.-])((?:knowledge|notes|reviews|showroom|docs|tokens)/[\w./-]+)")
FIGURE_RE = re.compile(r"\brc\s*=\s*\d+\b|\b\d[\d,]*\s+[a-zA-Z(][\w()-]*")


def is_mechanical(row):
    return (row.get("tag") in MECHANICAL_TAGS) or (row.get("verdict") in MECHANICAL_VERDICTS)


def commands(row):
    """Backticked strings whose head verb is a real tool. Prose in backticks is not a command."""
    out = []
    for c in CMD_RE.findall(row.get("evidence", "")):
        c = c.strip()
        head = c.split()[0] if c.split() else ""
        if head in VERBS:
            out.append(c)
    return out


GLOB_NEXT = ("*", "?", "[")
ELLIPSIS = "\u2026"
ABSENT_PREFIX = "absent:"
NONREPO_MARKER = "(NON-REPO:"
NONREPO_WINDOW = 60   # chars after the pointer in which the ruled s191-D2 marker must appear


def pointers(ev):
    """[(path, mode)] \u2014 every repo-relative pointer WITH the dialect it was written in (#208).

    mode is EXISTS   \u2014 the default: the path must exist on disk (the pre-#208 rule, unchanged)
           ABSENT   \u2014 written `absent:<path>`: the claim IS the absence, so the path must NOT
                      exist. The legal form for a finding whose subject is a missing file.
           NON-REPO \u2014 followed by the ruled `s191-D2` `(NON-REPO: <where>)` marker: the home is
                      DECLARED elsewhere, so this linter cannot and does not judge existence.
           PREFIX   \u2014 written with a trailing ellipsis: a TRUNCATION, resolved as a prefix
                      glob. At least one real path must start with it. #208 closes the
                      laundering hole where one keystroke excused any dead pointer.
    A `*`/`?`/`[` metacharacter still means PATTERN and is excluded entirely (see paths_in)."""
    return [(p, mode) for p, mode, _, _ in pointers_ex(ev)]


def paths_in(ev):
    """Repo-relative path POINTERS. A match followed by a glob metacharacter or an ellipsis is a
    PATTERN, not a pointer, and is excluded — `reviews/REVIEW-204-*.html` names a real family of
    files, and reporting it as a dead pointer is a false positive that would train a reader to
    ignore the check (found by driving this linter on the #204 tables, fix loop amendment ②)."""
    return [p for p, mode in pointers(ev) if mode == "EXISTS"]


# ---- #308 · JUDGE AT THE COMMIT, and the three misreads (s308-D29) ------------------------------
# Dave, 2026-09-29 13:09, on the old claim tables: "Lets do this properly, I'd rather rebuild than
# patch". The measured cause (lane C, #308): of nine red rows only TWO had gone stale — the other
# seven were the CHECKER misjudging rows that were true, or rows no checker can probe. So the fix is
# to the instrument's reading, not to the rows (ADR-0017 rule 3 freezes the rows anyway).

# An ABSENCE CLAIM written in words, attached to the pointer it follows: "`notes/x.md…`, a path
# that does not exist". Anchored at the pointer's end and deliberately narrow — a quoted error
# message that merely CONTAINS "does not exist" further along (W3-18) is not a claim about the path.
ABSENCE_RE = re.compile(
    r"^[`'\"…]*[\s,(]*"
    r"(?:(?:(?:a|the)\s+(?:path|file|directory|dir)\s+(?:that|which)\s+|which\s+|that\s+)?"
    r"(?:(?:does|did)\s+not|doesn't|didn't|never)\s+exist(?:s|ed)?\b"
    r"|(?:is|was)\s+absent\b)", re.I)

DECLARED_NOTES = "_declared-notes.jsonl"   # the sidecar beside the tables — see load_notes()
NOTE_FIELDS = ("table", "line", "id", "kind", "declared", "date", "ruling", "why")
NOTE_KINDS = ("UNPROBEABLE",)
SAMPLE_TIMEOUT = 30                         # seconds per re-run; the selftest shortens it


def pointers_ex(ev):
    """[(path, mode, start, is_prefix)] — `pointers()` with the pointer's offset kept (#308).

    The offset is what lets the linter tell a path the WRITER typed from a path the row QUOTES
    out of a tool's output (`output_tool`). `is_prefix` records a trailing ellipsis, so an absence
    claim about a truncated path is judged as a prefix too."""
    out = []
    for m in PATH_RE.finditer(ev):
        p = m.group(1)
        nxt = ev[m.end():m.end() + 1]
        if nxt in GLOB_NEXT or p.endswith("-") or p.endswith("/"):
            continue
        prefix = (nxt == ELLIPSIS)
        tail = ev[m.end():m.end() + NONREPO_WINDOW]
        if NONREPO_MARKER in tail:
            mode = "NON-REPO"
        elif ev[max(0, m.start() - len(ABSENT_PREFIX)):m.start()] == ABSENT_PREFIX:
            mode = "ABSENT"
        elif ABSENCE_RE.match(tail):
            mode = "ABSENT"     # #308 W2-13: the row SAYS, in words, that this path does not exist
        elif prefix:
            mode = "PREFIX"
        else:
            mode = "EXISTS"
        out.append((p, mode, m.start(), prefix))
    return out


def output_tool(ev, pos):
    """The script whose OUTPUT the pointer at `pos` is quoted from, or None (#308, L1-1).

    THE RULE: a backticked span that is not itself a command, and comes after a command span in
    the same evidence, is that command's OUTPUT; the tool is the first `.py`/`.sh` operand of the
    nearest preceding command. A path the writer typed in prose is never tool output."""
    tool, seen_cmd = None, False
    for m in CMD_RE.finditer(ev):
        body = m.group(1).strip()
        words = body.split()
        if words and words[0] in VERBS:
            seen_cmd = True
            tool = next((t for t in words[1:] if t.endswith((".py", ".sh"))), None)
            continue
        if m.start() < pos < m.end():
            return tool if seen_cmd else None
    return None


def tool_bases(tool):
    """A tool's own directory and each ancestor below the repo root, nearest first.

    A path quoted from a tool's output resolves against THAT TOOL'S working base, and a tool
    names its outputs relative to where it lives: `knowledge/tokens/_build_blast_radius.py`
    prints `tokens/_blast-radius.json`, meaning `knowledge/tokens/_blast-radius.json` (#308 L1-1,
    both rows). Only these directories are tried, and only after the repo root fails."""
    out, d = [], os.path.dirname(tool or "")
    while d and d not in (".", "/"):
        out.append(d)
        d = os.path.dirname(d)
    return out


def _scratch_base(need):
    """Where a commit's tree may be materialised: the first candidate with room for `need` bytes.

    TMPDIR when set (CI; the render seat's convention), then /dev/shm, then the system default.
    ⚠ Measured at #308: the Cowork seat's home disk had 126 MB free at 99% use, and one commit's
    tree is ~84 MB — so the home disk is tried LAST and a tree is never written where it would
    fill the disk. No candidate with room is COULD-NOT-ASK, never a partial checkout."""
    cands = []
    if os.environ.get("TMPDIR"):
        cands.append(os.environ["TMPDIR"])
    cands += ["/dev/shm", tempfile.gettempdir()]
    for c in cands:
        try:
            if os.path.isdir(c) and os.access(c, os.W_OK) and \
                    shutil.disk_usage(c).free >= need * 1.25 + 32 * 2 ** 20:
                return c
        except OSError:
            continue
    return None


class History:
    """#308 (s308-D29, part a) — JUDGE EACH ROW AGAINST THE TREE THAT WROTE IT.

    A claim row is a dated record (ADR-0017 rule 3): it asserts what was true WHEN IT WAS WRITTEN.
    Judging it against today's tree calls every later edit a lie — WIRE-14 (127 steps at 9d552ddc,
    166 today) and WIRE-21 (3 × `fetch-depth: 0` then, 4 since 801fe7cc) were exactly that.

      · commit_of(row) — `git blame --porcelain` on the table, per LINE, because one table
        (206-w45) was written in two commits. None means JUDGE THE WORKING TREE: a row not yet
        committed, a table outside this repo, or no git — the pre-#308 behaviour, never a guess.
      · exists / prefix_exists — pointers resolved in `git ls-tree -r <sha>` (one call per commit,
        cached; the same answer `git cat-file -e <sha>:<path>` gives, without a call per path).
      · workdir(sha) — a row's command is RE-RUN in that commit's tree. ONE throwaway clone per
        run, `--shared` (it borrows this repo's objects read-only), checked out DETACHED and
        switched commit to commit. ⛔ NOT `git worktree add` on this repo: that writes
        `.git/worktrees/<id>/` INSIDE the repo and `worktree remove`/`prune` must unlink it
        there — which the Cowork mount refuses (deletes are off; the stranded-`index.lock`
        class). The clone lives outside the repo and is removed whole by close().
    `at_head=True` (`--at-head`) switches all of this off: the pre-#308 reading, kept so the two
    can be compared on the same tables."""

    def __init__(self, root, at_head=False):
        self.root = os.path.abspath(root)
        self.at_head = at_head
        self._blame, self._trees = {}, {}
        self._tmp = self._clone = self._checked = None
        self._runtmp = None
        self.git = shutil.which("git") is not None
        self.shallow = False
        if self.git and not at_head:
            p = self._git("rev-parse", "--is-shallow-repository")
            self.shallow = p.returncode == 0 and p.stdout.strip() == "true"

    def _git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True,
                              stdin=subprocess.DEVNULL)

    def _in_clone(self, *args):
        # ⛔ Every command that WRITES runs here, and only ever inside the throwaway clone. A
        # `clean -fdx` with the wrong cwd would be aimed at the real repo, so the guard is explicit.
        if not (self._clone and self._tmp and os.path.abspath(self._clone).startswith(
                os.path.abspath(self._tmp) + os.sep)):
            raise RuntimeError("refusing a write-side git call outside the throwaway clone")
        return subprocess.run(["git", *args], cwd=self._clone, capture_output=True, text=True,
                              stdin=subprocess.DEVNULL)

    def commit_of(self, row):
        if self.at_head or not self.git or "_src" not in row:
            return None
        src = os.path.abspath(row["_src"])
        rel = os.path.relpath(src, self.root)
        if rel.startswith(".."):
            return None
        if src not in self._blame:
            p = self._git("blame", "--porcelain", "--", rel)
            m = {}
            if p.returncode == 0:
                for line in p.stdout.splitlines():
                    f = line.split()
                    if len(f) >= 3 and len(f[0]) == 40 and \
                            all(c in "0123456789abcdef" for c in f[0]) and f[2].isdigit():
                        m[int(f[2])] = f[0]
            self._blame[src] = m
        sha = self._blame[src].get(row.get("_lineno"))
        if sha is None or set(sha) == {"0"}:
            return None
        return sha

    def _tree(self, sha):
        if sha not in self._trees:
            p = subprocess.run(["git", "ls-tree", "-r", "-l", "-z", "--full-tree", sha],
                               cwd=self.root, capture_output=True, stdin=subprocess.DEVNULL)
            files, dirs, size = set(), set(), 0
            for ent in p.stdout.decode("utf-8", "replace").split("\0"):
                meta, _, path = ent.partition("\t")
                if not path:
                    continue
                parts = meta.split()
                if len(parts) >= 4 and parts[3].isdigit():
                    size += int(parts[3])
                files.add(path)
                segs = path.split("/")
                for i in range(1, len(segs)):
                    dirs.add("/".join(segs[:i]))
            self._trees[sha] = (files, dirs, size, p.returncode == 0)
        return self._trees[sha]

    def exists(self, sha, rel):
        if sha is None:
            return os.path.exists(os.path.join(self.root, rel))
        files, dirs, _, _ = self._tree(sha)
        rel = os.path.normpath(rel)
        return rel in files or rel in dirs

    def prefix_exists(self, sha, prefix):
        if sha is None:
            return bool(glob.glob(glob.escape(os.path.join(self.root, prefix)) + "*"))
        files, dirs, _, _ = self._tree(sha)
        return any(f.startswith(prefix) for f in files) or any(d.startswith(prefix) for d in dirs)

    def has_module(self, sha, name):
        """Is `name` a module IN THE TREE (a local file), as opposed to a third-party install?"""
        if sha is None:
            files = self._tree("HEAD")[0] if self.git else set()
            if not files:
                return any(os.path.exists(os.path.join(self.root, d, name + ".py"))
                           for d in ("", "knowledge"))
        else:
            files = self._tree(sha)[0]
        return any(os.path.basename(f) == name + ".py" or ("/%s/__init__.py" % name) in "/" + f
                   for f in files)

    def workdir(self, sha):
        """(dir, None) to run a row's command in, or (None, reason) — the reason is COULD-NOT-ASK."""
        if sha is None:
            return self.root, None
        if self._checked == sha:
            return self._clone, None
        _, _, size, ok = self._tree(sha)
        if not ok:
            return None, "commit %s is not readable here (`git ls-tree` failed)" % sha[:8]
        try:
            if self._clone is None:
                base = _scratch_base(size)
                if base is None:
                    return None, ("no scratch location has room to materialise %s (~%d MB) — "
                                  "refused rather than fill a disk" % (sha[:8], size // 2 ** 20))
                self._tmp = tempfile.mkdtemp(prefix="evidence-at-commit-", dir=base)
                self._clone = os.path.join(self._tmp, "tree")
                p = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout",
                                    self.root, self._clone], capture_output=True, text=True,
                                   stdin=subprocess.DEVNULL)
                if p.returncode:
                    self.close()
                    return None, "a --shared clone could not be made: %s" % p.stderr.strip()[:160]
            else:
                self._in_clone("clean", "-fdxq")
            p = self._in_clone("-c", "advice.detachedHead=false", "checkout", "-q", "-f",
                               "--detach", sha)
            if p.returncode:
                self._checked = None
                return None, "checkout of %s failed: %s" % (sha[:8], p.stderr.strip()[:160])
        except (OSError, RuntimeError) as e:
            return None, "could not materialise %s: %s" % (sha[:8], e)
        self._checked = sha
        return self._clone, None

    def run_env(self):
        """The environment a re-run command gets: TMPDIR is a directory this run owns and
        removes, so an old selftest that never cleaned its own scratch (the pre-#308 version of
        this very file's selftest was one) cannot leave it behind on the seat. tiktoken's cache
        keeps its usual home, so a re-run never re-downloads an encoding."""
        env = dict(os.environ)
        try:
            if self._runtmp is None:
                self._runtmp = tempfile.mkdtemp(prefix="evidence-run-",
                                                dir=_scratch_base(0) or tempfile.gettempdir())
            env.setdefault("TIKTOKEN_CACHE_DIR",
                           os.path.join(tempfile.gettempdir(), "data-gym-cache"))
            env["TMPDIR"] = self._runtmp
        except OSError:
            pass
        return env

    def close(self):
        for d in (self._tmp, self._runtmp):
            if d:
                shutil.rmtree(d, ignore_errors=True)
        self._tmp = self._clone = self._checked = self._runtmp = None


_NOMOD_RE = re.compile(r"No module named '([\w.]+)'")


def env_failure(rc, out, err, declared, hist=None, sha=None):
    """#308 — WHY a re-run is COULD-NOT-ASK rather than a mismatch, or None.

    ⛔ The false-red risk Dave was told about: an old command re-run today can fail for reasons
    that say nothing about the row. Exactly four readings are ENVIRONMENTAL, and each is named:
      1. rc=77 — the command itself answered COULD-NOT-ASK (`_could_not_ask.py`), e.g. WIRE-20 in
         CI, where evidence pointers `_governs.py` reads are not in the checkout;
      2. rc=127 / rc=126 — the shell could not find, or could not execute, a tool;
      3. `No module named 'x'` where `x` is NOT a file in that commit's tree — a third-party
         dependency missing or changed here. (A LOCAL module that fails to import is the code's
         own defect at that commit, and stays a MISMATCH.)
      4. a timeout — handled by the caller, which never waits past SAMPLE_TIMEOUT.
    Everything else that diverges is a MISMATCH. A declared rc that matches is never excused."""
    if declared is not None and rc == declared:
        return None
    if rc == CNA.EXIT:
        return ("the command answered COULD-NOT-ASK itself (rc=%d)%s" %
                (rc, ": " + (CNA.reason_in((out or "") + "\n" + (err or "")) or "")[:140]
                 if CNA.reason_in((out or "") + "\n" + (err or "")) else ""))
    if rc in (126, 127):
        return ("rc=%d — the shell could not %s a tool the command names"
                % (rc, "execute" if rc == 126 else "find"))
    m = _NOMOD_RE.search(err or "")
    if m:
        top = m.group(1).split(".")[0]
        if not (hist and hist.has_module(sha, top)):
            return ("Python module %r is not installed here and is not a file in the tree — a "
                    "missing or changed DEPENDENCY, not a defect of the row" % top)
    return None


def load_notes(rows):
    """#308 (s308-D29, part b) — DECLARED NOTES, read from a SIDECAR beside the tables.

    WHERE, and why not in the table: the tables are dated period records (ADR-0017 rule 3). A note
    appended INTO one would change the file's blob, so "this table is byte-identical to what its
    wave wrote" would stop being provable by git, and it would need a new row `kind` in the shared
    `_claimtable` schema. The sidecar `notes/_claims/_declared-notes.jsonl` is the note's ONE home
    (rule 1), each note carries an ADDRESS — table, line, id, kind — and this function is its
    RESOLVER, landed with it (rule 2): an address whose line does not hold that id is a HARD FAIL.
    Notes are added, never edited; the file is append-only.

    Returns ({(abs table path, line): note}, [(label, reason)])."""
    notes, fails, dirs, loaded = {}, [], set(), {}
    for r in rows:
        if "_src" in r:
            dirs.add(os.path.dirname(os.path.abspath(r["_src"])))
    for d in sorted(dirs):
        path = os.path.join(d, DECLARED_NOTES)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for n, raw in enumerate(f, 1):
                s = raw.strip()
                if not s or s.startswith("//"):
                    continue
                label = "%s:%d" % (DECLARED_NOTES, n)
                try:
                    note = json.loads(s)
                except Exception as e:
                    fails.append((label, "DECLARED NOTE is not valid JSON — %s" % e))
                    continue
                missing = [k for k in NOTE_FIELDS if note.get(k) in (None, "")]
                if missing:
                    fails.append((label, "DECLARED NOTE lacks %s — a declaration must say what, "
                                         "where, when, under which ruling and why"
                                  % ", ".join(missing)))
                    continue
                if note["declared"] not in NOTE_KINDS:
                    fails.append((label, "DECLARED NOTE says %r; the only declaration this linter "
                                         "honours is %s" % (note["declared"], "/".join(NOTE_KINDS))))
                    continue
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(note["date"])):
                    fails.append((label, "DECLARED NOTE date %r is not YYYY-MM-DD" % note["date"]))
                    continue
                table = os.path.join(d, note["table"])
                if table not in loaded:
                    loaded[table] = ({r["_lineno"]: r for r in CT.load(table)[0]}
                                     if os.path.exists(table) else None)
                held = loaded[table]
                row = held.get(note["line"]) if held is not None else None
                if row is None or row["id"] != note["id"] or row.get("kind") != note["kind"]:
                    fails.append((note["id"], "STALE NOTE ADDRESS: %s names %s line %s as %s %r, "
                                  "but %s — an address nothing resolves is worse than a copy "
                                  "(ADR-0017 rule 2)"
                                  % (label, note["table"], note["line"], note["kind"], note["id"],
                                     "the table does not exist" if held is None else
                                     "that line holds no row" if row is None else
                                     "that line holds %s %r" % (row.get("kind"), row["id"]))))
                    continue
                notes[(table, note["line"])] = note
    return notes, fails


def tokens(row):
    ev = row.get("evidence", "")
    cmds = commands(row)
    paths = pointers(ev)
    figs = FIGURE_RE.findall(ev)
    return cmds, paths, figs


def lint(rows, hist=None, declared=None, info=None):
    """[(id, reason)] — one entry per s182-D1 failure. Empty == conformant.

    #308: every pointer is judged in the tree of the commit that WROTE its row (`History`); a
    path quoted from a tool's OUTPUT falls back to that tool's base; an absence stated in words
    is judged as an absence; and a token-less row is excused ONLY by a DECLARED note, which is
    appended to `declared` (and counted by the caller), never folded into a pass. `info` collects
    the non-failing readings worth printing (tool-base resolutions, unused notes)."""
    own = hist is None
    hist = hist or History(ROOT)
    declared = declared if declared is not None else []
    info = info if info is not None else []
    try:
        notes, fails = load_notes(rows)
        used = set()
        for r in rows:
            ev = r.get("evidence", "")
            sha = hist.commit_of(r)
            at = "" if sha is None else " (judged at %s, the commit that wrote this row)" % sha[:8]
            cmds, figs = commands(r), FIGURE_RE.findall(ev)
            ptrs = pointers_ex(ev)
            for p, mode, pos, prefix in ptrs:
                p2 = p.rstrip(".,;:)")
                rel = p2.split(":")[0]
                if mode == "NON-REPO":
                    continue      # s191-D2: the home is DECLARED elsewhere; not this linter's to judge
                if mode == "ABSENT":
                    present = hist.prefix_exists(sha, rel) if prefix else hist.exists(sha, rel)
                    if not present and ev[max(0, pos - len(ABSENT_PREFIX)):pos] != ABSENT_PREFIX:
                        info.append((r["id"], "`%s` is claimed ABSENT in words, and is absent%s"
                                     % (p2, at or " from the working tree")))
                    if present:
                        fails.append((r["id"], "FALSE ABSENCE: evidence declares `%s` absent, but "
                                               "that path EXISTS%s — an absence claim whose subject "
                                               "is present is the same defect as a dead pointer, "
                                               "mirrored" % (p2, at)))
                    continue
                probe = hist.prefix_exists if mode == "PREFIX" else hist.exists
                if probe(sha, rel):
                    continue
                tool = output_tool(ev, pos)
                base = next((b for b in tool_bases(tool)
                             if probe(sha, os.path.join(b, rel))), None) if tool else None
                if base:
                    info.append((r["id"], "`%s` is quoted from %s's OUTPUT and resolves against "
                                          "the tool's base %s/ → %s%s"
                                 % (p2, os.path.basename(tool), base, os.path.join(base, rel), at)))
                    continue
                if mode == "PREFIX":
                    # #208: a trailing ellipsis is a TRUNCATION, not a licence. Resolve it.
                    fails.append((r["id"], "DEAD POINTER (truncated): evidence names `%s…`, and NO "
                                           "path starts with it%s — the trailing ellipsis does not "
                                           "make a dead pointer legal (#208 laundering hole). Write "
                                           "the full path, or `absent:%s` if the ABSENCE is the "
                                           "claim, or add the ruled `(NON-REPO: <where>)` marker"
                                  % (p2, at, p2)))
                else:
                    fails.append((r["id"], "DEAD POINTER: evidence names `%s`, which does not "
                                           "exist%s — a dead pointer reads as evidence. If the "
                                           "ABSENCE is the claim, write `absent:%s`; if the file "
                                           "lives outside the repo, use the ruled s191-D2 marker "
                                           "`(NON-REPO: <where>)`" % (p2, at, p2)))
            if not is_mechanical(r):
                continue
            if not (cmds or ptrs or figs):
                key = (os.path.abspath(r["_src"]), r["_lineno"]) if "_src" in r else None
                note = notes.get(key)
                if note:
                    used.add(key)
                    declared.append((r["id"], note))
                    continue
                fails.append((r["id"], "s182-D1: MECHANICAL row (tag=%s verdict=%s) carries NO "
                                       "probeable token — no command, no existing path, no figure "
                                       "— and no DECLARED note in %s names it. Evidence: %r"
                              % (r.get("tag"), r.get("verdict"), DECLARED_NOTES,
                                 r.get("evidence", "")[:90])))
        for key, note in sorted(notes.items()):
            if key not in used:
                info.append((note["id"], "UNUSED NOTE: %s line %s is not token-less (or not "
                                         "mechanical) in this reading, so its note declares "
                                         "nothing — kept, because notes are added, never edited"
                             % (note["table"], note["line"])))
        return fails
    finally:
        if own:
            hist.close()


def _without_paths(cmd):
    """The command with its PATH-LIKE operands removed (#208).

    An UNSAFE marker inside a FILE NAME is a name, not an action: `grep -c X
    knowledge/_git_commit.sh` was refused as UNSAFE because the substring `commit` appears in
    the path, which made every claim about the commit script structurally unverifiable. Verbs
    are still matched on the operand-free command, so `git commit -m …` is refused exactly as
    before. Redirects and `$(`/backtick substitution are matched on the FULL string — those are
    shell syntax, not operands."""
    return " ".join(t for t in cmd.split()
                    if not ("/" in t or t.endswith(".py") or t.endswith(".sh")
                            or t.endswith(".jsonl") or t.endswith(".json")
                            or t.endswith(".md") or t.endswith(".yml")))


SHELL_MARKERS = (">", ">>", "|& ", "$(", "`")


def classify(cmd):
    """(verdict, reason). verdict ∈ RUNNABLE | SIDE-EFFECTS | UNSAFE | NOT-IN-ENV."""
    head = cmd.split()[0]
    stripped = _without_paths(cmd)
    for m in UNSAFE_MARKERS:
        if m in (cmd if m in SHELL_MARKERS else stripped):
            return "UNSAFE", "contains %r — arbitrary effect, no allowlist can vouch for it" % m
    if head in ("python3", "python"):
        if " -c" in cmd:
            return "UNSAFE", "`python3 -c` runs arbitrary code — cannot be judged read-only"
        if "--check" in cmd or "--selftest" in cmd or "--dry-run" in cmd:
            pass
        elif "--run" in cmd and "_probe_registry/" in cmd:
            # #208 verifier finding 8: `_registry.py --run [--probe P-N]` is a READ-ONLY probe
            # drive, and the classifier refused it purely for lacking a `--check`. The exception
            # is deliberately NARROW — it is keyed on the registry's own directory, not on the
            # word `--run`, which means nothing on its own anywhere else in this repo.
            pass
        else:
            return ("SIDE-EFFECTS",
                    "a bare `%s` REWRITES its tracked audit output; #204 declared this exact "
                    "stop. Only --check/--selftest/--dry-run forms are sampled" % head)
    elif head not in SAFE_VERBS:
        return "UNSAFE", "head verb %r is not on the read-only allowlist" % head
    if shutil.which(head) is None:
        return "NOT-IN-ENV", "%r is not on PATH in this environment — DECLARED gap, not a pass" % head
    return "RUNNABLE", ""


def observe(row, out):
    """#208 — compare an OBSERVATION, not an exit code. Returns [] or [reason].

    Only fires when the row DECLARED an expectation; a row without one is judged exactly as it
    was before (`rc` only), which is what keeps this a change BY ADDITION."""
    problems = []
    want = row.get("expect_stdout_contains")
    if want is not None and want not in out:
        problems.append("stdout does NOT contain %r (declared expect_stdout_contains). "
                        "First 120 chars of stdout: %r" % (want, out[:120]))
    if "expect_count" in row:
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        if not lines:
            problems.append("expect_count=%d declared, but the command printed NOTHING on "
                            "stdout — an empty observation is never a pass"
                            % row["expect_count"])
        else:
            try:
                got = int(lines[-1].split()[0])
            except (ValueError, IndexError):
                problems.append("expect_count=%d declared, but the last stdout line %r does not "
                                "parse as an integer — a count that cannot be read is a LOUD "
                                "failure, not a pass" % (row["expect_count"], lines[-1][:60]))
            else:
                if got != row["expect_count"]:
                    problems.append("expect_count=%d declared, command observed %d"
                                    % (row["expect_count"], got))
    return problems


def sample(rows, n, seed, strict=False, hist=None):
    """Seeded re-run of a subset. Returns (results, mismatches, refusals).

    #208: `mismatches` now carries BOTH kinds of divergence — an rc mismatch and an OBSERVATION
    mismatch — because both mean the same thing to a caller: the evidence no longer reproduces.
    #308: each drawn row is re-run IN THE TREE OF THE COMMIT THAT WROTE IT (`History.workdir`),
    and an environmental failure (`env_failure`, or a timeout, or a head verb not on PATH) is
    COULD-NOT-ASK — carried in `refusals` with that verdict, counted apart, never a pass and
    never a mismatch."""
    own = hist is None
    hist = hist or History(ROOT)
    try:
        return _sample(rows, n, seed, strict, hist)
    finally:
        if own:
            hist.close()


def _could_not(refusals, r, cmd, reason):
    refusals.append((r["id"], "COULD-NOT-ASK", cmd, reason))
    print("  ◌ COULD-NOT-ASK %s — `%s`\n      %s" % (r["id"], cmd[:80], reason))


def _sample(rows, n, seed, strict, hist):
    has_cmd = [r for r in rows if commands(r)]
    # #208: a row that DECLARED an expected observation asked to be checked. It is never left to
    # chance — it is drawn ALWAYS, on top of the seeded random draw over everything else.
    forced = [r for r in has_cmd if "expect_stdout_contains" in r or "expect_count" in r]
    pool = [r for r in has_cmd if r not in forced]
    rng = random.Random(seed)
    drawn = forced + (rng.sample(pool, min(n, len(pool))) if pool else [])
    drawn.sort(key=lambda r: r["id"])
    results, mismatches, refusals = [], [], []
    print("── SAMPLER · seed=%d · pool=%d row(s) with a command · %d with a declared observation "
          "(always drawn) · drawn=%d: %s"
          % (seed, len(has_cmd), len(forced), len(drawn),
             ", ".join(r["id"] for r in drawn) or "none"))
    # #308: run grouped by the commit that wrote each row, so each tree is materialised once.
    order = sorted(drawn, key=lambda r: (hist.commit_of(r) or "", r["id"]))
    current = object()
    for r in order:
        cmd = commands(r)[0]
        sha = hist.commit_of(r)
        if sha != current:
            current = sha
            print("  ── at %s" % ("the working tree" if sha is None else
                                 "%s — the tree that wrote these rows" % sha[:8]))
        verdict, reason = classify(cmd)
        if verdict == "NOT-IN-ENV":
            _could_not(refusals, r, cmd, "NOT-IN-ENV: " + reason)
            continue
        if verdict != "RUNNABLE":
            refusals.append((r["id"], verdict, cmd, reason))
            print("  ⛔ REFUSED [%s] %s — `%s`\n      %s" % (verdict, r["id"], cmd[:100], reason))
            continue
        wd, why = hist.workdir(sha)
        if wd is None:
            _could_not(refusals, r, cmd, why)
            continue
        try:
            p = subprocess.run(["bash", "-c", cmd], cwd=wd, capture_output=True, env=hist.run_env(),
                               text=True, timeout=SAMPLE_TIMEOUT, stdin=subprocess.DEVNULL)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            # An evidence command quoted without its file operand (`grep -c 'x'`) would read
            # stdin forever; stdin is closed above. #308: a timeout says the command did not
            # finish HERE — too slow for this machine or waiting on something absent — which is
            # not evidence about the row: COULD-NOT-ASK, never a pass and never a mismatch.
            _could_not(refusals, r, cmd, "TIMEOUT: no exit within %ds" % SAMPLE_TIMEOUT)
            continue
        except Exception as e:
            _could_not(refusals, r, cmd, "NOT-IN-ENV: execution raised %s" % e)
            continue
        declared = r.get("rc")
        env = env_failure(rc, p.stdout, p.stderr, declared, hist, sha)
        if env:
            _could_not(refusals, r, cmd, "ENVIRONMENT (rc=%d): %s" % (rc, env))
            continue
        results.append((r["id"], cmd, rc, declared))
        # #208: the OBSERVATION check runs first — it is the one that can see content.
        obs = observe(r, p.stdout or "")
        for reason in obs:
            mismatches.append((r["id"], cmd, rc, declared))
            print("  ⛔ OBSERVATION MISMATCH %s — `%s`\n      %s" % (r["id"], cmd[:80], reason))
        if declared is None:
            if not obs:
                print("  ⚠ RAN (no declared rc to compare) %s — `%s` → rc=%d"
                      % (r["id"], cmd[:80], rc))
        elif rc != declared:
            mismatches.append((r["id"], cmd, rc, declared))
            print("  ⛔ RC MISMATCH %s — `%s` → rc=%d, row declares rc=%d"
                  % (r["id"], cmd[:80], rc, declared))
        elif not obs:
            checked = " + OBSERVATION" if ("expect_stdout_contains" in r
                                           or "expect_count" in r) else ""
            print("  ✅ RAN %s — `%s` → rc=%d (matches declared%s)"
                  % (r["id"], cmd[:80], rc, checked))
    cna = [x for x in refusals if x[1] == "COULD-NOT-ASK"]
    pol = [x for x in refusals if x[1] != "COULD-NOT-ASK"]
    if refusals:
        print("── DECLARED GAP: %d of %d sampled row(s) were NOT judged — %d REFUSED by policy, "
              "%d COULD-NOT-ASK (environment). Neither is counted as a pass or as a mismatch."
              % (len(refusals), len(drawn), len(pol), len(cna)))
    return results, mismatches, refusals


def main(argv):
    paths = [a for a in argv if not a.startswith("--")]
    skip = set()
    for i, a in enumerate(argv):
        if a in ("--sample", "--seed") and i + 1 < len(argv):
            skip.add(argv[i + 1])
    paths = [p for p in paths if p not in skip]
    if not paths:
        # ⛔ #219 — A GATE THAT CANNOT BE INVOKED WITHOUT AN ARGUMENT CANNOT SHIP.
        # This gate was the first of the four s219-D5(Q5) reds. Every OTHER gate in the pack
        # carries a DEFAULT_TARGETS of its own; this one alone had none, so a runner that calls
        # the shipped gates the obvious way (`python3 <gate>`) got rc=2 — bad arguments, which is
        # not a verdict at all. Fixed at cause here rather than in the runner's call signature:
        # a gate should know where its own material lives.
        #   · The repo's own two invocations pass `notes/_claims` explicitly and are UNCHANGED.
        #   · Bare now defaults to that same conventional home, so the two agree by construction
        #     instead of by a copied string in a workflow file.
        #   · When the home is not there — which is the pack's case, and a fresh designer
        #     project's case, because `notes/` is deliberately OUT of the ship list — the answer
        #     is COULD-NOT-ASK (77), not FAIL. The gate has no rows to lint; it has not found a
        #     defect. Keyed on the UNREACHABLE INPUT and named, per `_could_not_ask.py`; NEVER on
        #     "am I in CI" [[gate-cannot-pass-in-one-environment]].
        # ⚠ The refusal is reproducible on any machine by taking notes/_claims away, and the
        # reachable side still bites: with the directory present a planted bad row still exits 1.
        default = os.path.join(ROOT, DEFAULT_CLAIMS)
        if not os.path.isdir(default):
            return CNA.refuse(
                "the evidence linter",
                "no claim table was named and the conventional home %s does not exist here — "
                "there are no evidence rows to lint (notes/ is out of the release ship list, so "
                "this is the expected reading in a packed or a fresh project). Name a "
                "<rows.jsonl> or a directory of them to ask this gate anything." % DEFAULT_CLAIMS)
        if not [f for f in glob.glob(os.path.join(default, "*.jsonl"))
                if os.path.basename(f) != DECLARED_NOTES]:
            return CNA.refuse(
                "the evidence linter",
                "%s exists but holds no *.jsonl claim table — nothing to lint yet." % DEFAULT_CLAIMS)
        print("no claim table named — defaulting to %s" % DEFAULT_CLAIMS)
        paths = [DEFAULT_CLAIMS]
    # #208 WIRING: `_build_all.py` runs steps with an arbitrary cwd, and the wave seam wants ONE
    # invocation over a whole directory of tables (the verifier had to `cat` three files into a
    # temp path to get past a 1:1 limit elsewhere). Both are resolved here, LOUDLY: a token that
    # names neither a real path nor a repo-relative one is a REFUSAL, never a silent skip.
    expanded, missing = [], []
    for p in paths:
        cand = p if os.path.exists(p) else os.path.join(ROOT, p)
        if not os.path.exists(cand):
            missing.append(p)
        elif os.path.isdir(cand):
            # #308: the declared-notes sidecar lives beside the tables and is not one of them.
            found = sorted(f for f in glob.glob(os.path.join(cand, "*.jsonl"))
                           if os.path.basename(f) != DECLARED_NOTES)
            if not found:
                missing.append(p + " (directory contains no *.jsonl)")
            expanded.extend(found)
        else:
            expanded.append(cand)
    if missing:
        sys.stderr.write("✖ REFUSED: no such claim table(s): %s\n" % ", ".join(missing))
        return 2
    paths = expanded
    n = int(argv[argv.index("--sample") + 1]) if "--sample" in argv else DEFAULT_SAMPLE
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else DEFAULT_SEED
    strict = "--strict-sample" in argv
    at_head = "--at-head" in argv

    rows, residual = [], 0
    for p in paths:
        rs, defects = CT.load(p)
        residual += CT.report_defects(defects, p)
        rows.extend(rs)
    print("evidence linter: %d row(s) from %d file(s) · %d mechanical"
          % (len(rows), len(paths), sum(1 for r in rows if is_mechanical(r))))

    import time as _time
    t0 = _time.time()
    hist = History(ROOT, at_head=at_head)
    try:
        if hist.shallow:
            # #308: judging at the commit needs the history that wrote each row. A shallow clone
            # would blame every row on its boundary commit — a wrong answer that looks right.
            return CNA.refuse(
                "the evidence linter",
                "this checkout is SHALLOW, so the commit that wrote each claim row is not "
                "reachable — rows are judged in the tree that wrote them (s308-D29). Check out "
                "with fetch-depth: 0 (both gates.yml jobs do), or pass --at-head for the "
                "pre-#308 reading against the working tree.")
        print("── reading: %s" % ("AT HEAD — every row judged against the working tree "
                                   "(--at-head, the pre-#308 reading)" if at_head else
                                   "AT THE COMMIT — every row judged in the tree of the commit "
                                   "that wrote it (s308-D29); an uncommitted row is judged in "
                                   "the working tree"))
        declared, info = [], []
        fails = lint(rows, hist, declared, info)
        for i, reason in fails:
            print("  ⛔ %s — %s" % (i, reason))
        for i, reason in info:
            print("  ↳ %s — %s" % (i, reason))
        print("── s182-D1 LINT: %d failure(s) · %d DECLARED (a dated note in %s, counted, "
              "not a pass)" % (len(fails), len(declared), DECLARED_NOTES))
        for i, note in declared:
            print("  ◇ DECLARED %s — %s line %s · %s · %s · %s"
                  % (i, note["table"], note["line"], note["date"], note["ruling"],
                     note["why"][:110]))

        mism, refus = [], []
        if "--no-sample" not in argv:
            _, mism, refus = sample(rows, n, seed, strict, hist)
    finally:
        hist.close()
    cna = [x for x in refus if x[1] == "COULD-NOT-ASK"]
    pol = [x for x in refus if x[1] != "COULD-NOT-ASK"]
    print("── COUNTS: %d lint fail · %d declared · %d rc/observation mismatch · %d could-not-ask · "
          "%d refused by policy · %d unparsed · wall %.1fs"
          % (len(fails), len(declared), len(mism), len(cna), len(pol), residual,
             _time.time() - t0))

    bad = len(fails) + residual + len(mism) + (len(refus) if strict else 0)
    if bad:
        print("⛔ EVIDENCE GATE FAIL — %d lint · %d unparsed · %d rc/observation mismatch%s"
              % (len(fails), residual, len(mism),
                 " · %d refusal(s) under --strict-sample" % len(refus) if strict else ""))
        return 1
    nobs = sum(1 for r in rows if "expect_stdout_contains" in r or "expect_count" in r)
    print("✅ EVIDENCE GATE PASS — every mechanical row carries a probeable token or a DECLARED "
          "note (%d); 0 rc/observation mismatch(es); %d row(s) carried a declared OBSERVATION and "
          "none that was asked diverged; %d COULD-NOT-ASK and %d policy refusal(s) — none of them "
          "counted as a pass." % (len(declared), nobs, len(cna), len(pol)))
    if not nobs:
        print("⚠ NOT ONE ROW declared an expected observation (`expect_stdout_contains` / "
              "`expect_count`). For read-style evidence this run proved the commands still RUN, "
              "not that they still SAY what the rows claim (#208, the exit-code blindness).")
    return 0


# ---- selftest: plant-then-detect BOTH directions -----------------------------------------------

def _row(i, **kw):
    return dict({"id": i, "kind": "claim", "claim": "c", "evidence": "`ls knowledge` -> rc=0",
                 "tag": "PROVEN", "rc": 0}, **kw)


def _selftest_308(fails):
    """#308 (s308-D29) — six arms, each with a PLANTED RED that must still bite. Driven in a
    throwaway git repo with two commits, so 'the tree that wrote the row' and 'today's tree'
    genuinely differ: commit 1 writes the file a row points at, commit 2 deletes it."""
    global SAMPLE_TIMEOUT
    import tempfile
    if shutil.which("git") is None:
        print("  ◌ COULD-NOT-ASK: the #308 arms need git on PATH, and it is not here — "
              "not run, not passed")
        return
    base = _scratch_base(8 * 2 ** 20) or tempfile.gettempdir()
    tmp = tempfile.mkdtemp(prefix="evidence-308-selftest-", dir=base)
    hist = hist_head = None
    saved_timeout = SAMPLE_TIMEOUT
    try:
        def g(*a):
            return subprocess.run(["git", *a], cwd=tmp, capture_output=True, text=True,
                                  stdin=subprocess.DEVNULL)

        def put(rel, text):
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)

        g("init", "-q")
        for k, v in (("user.email", "selftest@apollo.invalid"), ("user.name", "evidence selftest"),
                     ("commit.gpgsign", "false")):
            g("config", k, v)
        put("knowledge/a_9f3a.txt", "x\n")
        put("knowledge/tokens/_tool_9f3a.py", "print('ok')\n")
        put("knowledge/tokens/_out_9f3a.json", "{}\n")
        put("knowledge/needs_mod_9f3a.py", "import no_such_module_9f3a\n")
        put("knowledge/local_9f3a.py", "import helper_9f3a\n")
        put("docs/helper_9f3a.py", "X = 1\n")      # IN the tree, but not importable from knowledge/
        put("knowledge/cna_9f3a.py", "import sys\nprint('COULD-NOT-ASK: x — input absent')\n"
                                     "sys.exit(77)\n")
        put("knowledge/fails_9f3a.py", "import sys\nsys.exit(1)\n")
        put("knowledge/sleeps_9f3a.py", "import time\ntime.sleep(6)\n")
        R = lambda i, ev, **kw: dict({"id": i, "kind": "claim", "claim": "c", "evidence": ev,
                                      "tag": "PROVEN"}, **kw)
        table = [
            R("J-1", "knowledge/a_9f3a.txt holds one x: `grep -c x knowledge/a_9f3a.txt`",
              rc=0, expect_count=1),
            R("J-2", "knowledge/never_9f3a.txt:3"),                                   # planted
            R("J-3", "`grep -c x knowledge/a_9f3a.txt`", rc=0, expect_count=5),      # planted
            R("V-1", "`python3 knowledge/needs_mod_9f3a.py --selftest` -> rc=0", rc=0),
            R("V-2", "`python3 knowledge/cna_9f3a.py --selftest` -> rc=0", rc=0),
            R("V-3", "`python3 knowledge/sleeps_9f3a.py --selftest` -> rc=0", rc=0),
            R("V-4", "`python3 knowledge/fails_9f3a.py --selftest` -> rc=0", rc=0),   # planted
            R("V-5", "`python3 knowledge/local_9f3a.py --selftest` -> rc=0", rc=0),   # planted
            R("A-1", "fed it (`notes/x_9f3a.md…`, a path that does not exist) -> rc=2"),
            R("A-2", "(`knowledge/tokens/_out_9f3a.json`, a path that does not exist)"),  # planted
            R("A-3", "`knowledge/tokens/_out_9f3a.json` returned rc=1 'DEAD POINTER ... does "
                     "not exist on disk'"),
            R("T-1", "`python3 knowledge/tokens/_tool_9f3a.py --check` → rc=0 · "
                     "`✓ PASS — tokens/_out_9f3a.json matches`"),
            R("T-2", "`python3 knowledge/tokens/_tool_9f3a.py --check` → rc=0 · "
                     "`✓ PASS — tokens/_nope_9f3a.json matches`"),                    # planted
            R("T-3", "the tool wrote tokens/_out_9f3a.json, I read it"),              # planted
            R("N-1", "the verbatim gate line in J-1"),
            R("N-2", "the verbatim gate line in the row above, again"),                         # planted
            R("N-3", "knowledge/gone_9f3a.md"),                                       # planted
        ]
        put("notes/_claims/t.jsonl", "".join(json.dumps(r) + "\n" for r in table))
        line = {r["id"]: i + 1 for i, r in enumerate(table)}
        note = lambda i, ln, **kw: json.dumps(dict({
            "table": "t.jsonl", "line": ln, "id": i, "kind": "claim", "declared": "UNPROBEABLE",
            "date": "2026-09-29", "ruling": "s308-D29", "why": "cites another row"}, **kw))
        put("notes/_claims/" + DECLARED_NOTES, "\n".join([
            note("N-1", line["N-1"]),
            note("N-3", line["N-3"]),                       # a note must NOT launder a dead pointer
            note("N-9", line["J-1"]),                       # planted: stale address
        ]) + "\n")
        g("add", "-A")
        g("commit", "-q", "-m", "one")
        g("rm", "-q", "knowledge/a_9f3a.txt")
        g("commit", "-q", "-m", "two — the file J-1 points at is gone from today's tree")

        rows, _ = CT.load(os.path.join(tmp, "notes", "_claims", "t.jsonl"))
        by = {r["id"]: r for r in rows}
        pick = lambda *ids: [by[i] for i in ids]
        hist = History(tmp)
        hist_head = History(tmp, at_head=True)

        def ids_of(xs):
            return {x[0] for x in xs}

        # ① JUDGE AT THE COMMIT — J-1 is true where it was written and false today.
        got = ids_of(lint(pick("J-1", "J-2"), hist))
        got_head = ids_of(lint(pick("J-1"), hist_head))
        _, mism, _ = sample(pick("J-1", "J-3"), 9, 205, hist=hist)
        if "J-1" in got or "J-1" in ids_of(mism):
            fails.append("JUDGE-AT-COMMIT: a row true in the tree that wrote it was failed "
                         "(lint %r, sample %r)" % (got, ids_of(mism)))
        elif "J-1" not in got_head:
            fails.append("JUDGE-AT-COMMIT CONTROL: --at-head did not fail J-1, so the arm cannot "
                         "tell the commit's tree from today's")
        elif "J-2" not in got or "J-3" not in ids_of(mism):
            fails.append("JUDGE-AT-COMMIT PLANTED RED: a pointer dead in its own commit (J-2) or "
                         "a count wrong in its own commit (J-3) was passed")
        else:
            print("  ✅ judge-at-commit arm: J-1 passes in the tree that wrote it (and fails "
                  "--at-head); planted J-2 dead pointer and J-3 wrong count still bite")

        # ② ENVIRONMENT → COULD-NOT-ASK, never a mismatch; a real failure stays a mismatch.
        SAMPLE_TIMEOUT = 2
        _, mism, refus = sample(pick("V-1", "V-2", "V-3", "V-4", "V-5"), 9, 205, hist=hist)
        cna = {i for i, v, _, _ in refus if v == "COULD-NOT-ASK"}
        if cna != {"V-1", "V-2", "V-3"}:
            fails.append("ENV → COULD-NOT-ASK: want V-1 (missing dependency), V-2 (rc=77), V-3 "
                         "(timeout); got %r" % sorted(cna))
        elif ids_of(mism) != {"V-4", "V-5"}:
            fails.append("ENV PLANTED RED: a plain rc=1 (V-4) and a LOCAL module that fails to "
                         "import (V-5) must stay MISMATCHES; got %r" % sorted(ids_of(mism)))
        elif env_failure(127, "", "bash: nosuch: command not found", 0) is None:
            fails.append("ENV: rc=127 was not read as an environmental failure")
        else:
            print("  ✅ env arm: missing dependency, rc=77 and a timeout are COULD-NOT-ASK; planted "
                  "rc=1 and a broken LOCAL import are still MISMATCHES")
        SAMPLE_TIMEOUT = saved_timeout

        # ③ ABSENCE stated in words.
        got = ids_of(lint(pick("A-1", "A-2", "A-3"), hist))
        if "A-1" in got or "A-3" in got:
            fails.append("ABSENCE: an absence claim in words (A-1) or a quoted message that merely "
                         "contains 'does not exist' (A-3) was failed: %r" % sorted(got))
        elif "A-2" not in got:
            fails.append("ABSENCE PLANTED RED: 'a path that does not exist' on a path that EXISTS "
                         "(A-2) was passed")
        else:
            print("  ✅ absence arm: 'a path that does not exist' is judged as an absence; planted "
                  "A-2 (present path) is FALSE ABSENCE; a quoted message is not a claim")

        # ④ A PATH QUOTED FROM A TOOL'S OUTPUT resolves against the tool's base.
        got = ids_of(lint(pick("T-1", "T-2", "T-3"), hist))
        if "T-1" in got:
            fails.append("TOOL-BASE: `tokens/_out_9f3a.json` quoted from knowledge/tokens/"
                         "_tool_9f3a.py's output was called dead")
        elif not {"T-2", "T-3"} <= got:
            fails.append("TOOL-BASE PLANTED RED: a dead path in tool output (T-2) or the same path "
                         "typed in PROSE (T-3) was passed — the fallback is too wide: %r"
                         % sorted(got))
        else:
            print("  ✅ tool-base arm: a tool's quoted output resolves against the tool's base; "
                  "planted T-2 (dead in output) and T-3 (same path in prose) still bite")

        # ⑤ + ⑥ DECLARED NOTES — honoured, counted, and nothing more.
        dec, info = [], []
        got = ids_of(lint(pick("N-1", "N-2", "N-3"), hist, dec, info))
        if "N-1" in got or [i for i, _ in dec] != ["N-1"]:
            fails.append("DECLARED NOTE: N-1's note was not honoured as a counted DECLARED skip "
                         "(fails %r, declared %r)" % (sorted(got), [i for i, _ in dec]))
        elif "N-2" not in got:
            fails.append("UNDECLARED: a token-less mechanical row with NO note (N-2) was passed")
        elif "N-3" not in got:
            fails.append("NOTE LAUNDERING: an UNPROBEABLE note excused a DEAD POINTER (N-3)")
        elif "N-9" not in got:
            fails.append("STALE NOTE: a note addressed to a line holding another id was honoured")
        else:
            print("  ✅ declared-note arm: N-1's dated note is honoured and COUNTED; planted N-3 "
                  "(dead pointer under a note) and N-9 (stale address) still bite")
            print("  ✅ undeclared arm: a token-less mechanical row with no note (N-2) is still "
                  "REFUSED under s182-D1")
    finally:
        SAMPLE_TIMEOUT = saved_timeout
        for h in (hist, hist_head):
            if h:
                h.close()
        shutil.rmtree(tmp, ignore_errors=True)


def selftest():
    global ROOT                      # #219 no-material arm repoints it at a throwaway tree
    import tempfile
    fails = []
    tmp = tempfile.mkdtemp(prefix="evidence-selftest-")

    def write(name, rows):
        p = os.path.join(tmp, name)
        with open(p, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        return p

    # --- direction 1: PLANT the three lint classes ---
    plants = [
        ("token-less mechanical row",
         _row("E-1", evidence="I looked at it and it seemed right"),
         "s182-D1"),
        ("dead path pointer",
         _row("E-2", evidence="knowledge/_this_file_does_not_exist_9f3a.py:12"),
         "DEAD POINTER"),
    ]
    for label, row, marker in plants:
        rows, _ = CT.load(write("p.jsonl", [row]))
        got = lint(rows)
        if not any(marker in r for _, r in got):
            fails.append("PLANT NOT CAUGHT: %s (expected %s, got %r)" % (label, marker, got))
        else:
            print("  ✅ plant caught (%s): %s" % (label, got[0][1][:70]))

    # exempt arm: the SAME token-less evidence on an UNPROVEN row must NOT fail
    rows, _ = CT.load(write("x.jsonl", [_row("E-3", tag="UNPROVEN",
                                             evidence="named, not established — a declared stop")]))
    if lint(rows):
        fails.append("FALSE POSITIVE: an UNPROVEN row was required to carry a mechanical token — "
                     "that manufactures false provenance")
    else:
        print("  ✅ exempt arm: an UNPROVEN row is not forced to carry a probeable token")

    # glob arm: a PATTERN must not be reported as a dead pointer, but a real dead path must be
    rows, _ = CT.load(write("glob.jsonl", [_row("E-8", evidence="`ls reviews/REVIEW-204-*.html`")]))
    if any("DEAD POINTER" in r for _, r in lint(rows)):
        fails.append("FALSE POSITIVE: a glob PATTERN was reported as a dead pointer: %r"
                     % lint(rows))
    else:
        print("  ✅ glob arm: `reviews/REVIEW-204-*.html` is a pattern, not a dead pointer")
    rows, _ = CT.load(write("glob2.jsonl", [_row("E-9",
                            evidence="reviews/REVIEW-204-nope-9f3a.html")]))
    if not any("DEAD POINTER" in r for _, r in lint(rows)):
        fails.append("GLOB EXCLUSION TOO WIDE: a genuinely dead path under the same prefix was "
                     "no longer flagged")
    else:
        print("  ✅ glob arm (other direction): a genuinely dead path is still flagged")

    # --- #208 ABSENCE dialect: both directions ---
    rows, _ = CT.load(write("abs1.jsonl", [_row("E-10",
                            evidence="the gate has no hatch: `absent:knowledge/_no_such_9f3a.py`")]))
    if lint(rows):
        fails.append("ABSENCE: an `absent:` pointer at a genuinely missing path was still a "
                     "failure — the honest statement has no legal form: %r" % lint(rows))
    else:
        print("  ✅ absence arm: `absent:<missing path>` is LEGAL — the claim IS the absence")
    rows, _ = CT.load(write("abs2.jsonl", [_row("E-11",
                            evidence="`absent:knowledge/_validate_evidence.py`")]))
    if not any("FALSE ABSENCE" in r for _, r in lint(rows)):
        fails.append("ABSENCE (other direction): `absent:` on a path that EXISTS was not caught "
                     "— an absence claim whose subject is present must fail like a dead pointer")
    else:
        print("  ✅ absence arm (other direction): `absent:` on an EXISTING path is FALSE ABSENCE")

    # --- #208 s191-D2 NON-REPO marker, and the ellipsis LAUNDERING HOLE it replaces ---
    rows, _ = CT.load(write("nr.jsonl", [_row("E-12",
                            evidence="notes/_vfy_9f3a.txt (NON-REPO: /sessions/x/vfy/full)")]))
    if lint(rows):
        fails.append("s191-D2: the ruled `(NON-REPO: <where>)` marker was not honoured: %r"
                     % lint(rows))
    else:
        print("  ✅ s191-D2 arm: a pointer with the ruled `(NON-REPO: …)` marker is legal")
    rows, _ = CT.load(write("ell.jsonl", [_row("E-13", evidence="notes/_vfy_9f3a.txt…")]))
    if not any("truncated" in r for _, r in lint(rows)):
        fails.append("LAUNDERING HOLE OPEN: a trailing ellipsis still excuses a dead pointer — "
                     "one keystroke past the gate is the hole #208 found")
    else:
        print("  ✅ ellipsis arm: a truncated pointer matching NOTHING is a DEAD POINTER")
    rows, _ = CT.load(write("ell2.jsonl", [_row("E-14", evidence="knowledge/_validate_evid…")]))
    if lint(rows):
        fails.append("ELLIPSIS TOO TIGHT: a truncation that DOES resolve to a real file was "
                     "reported dead: %r" % lint(rows))
    else:
        print("  ✅ ellipsis arm (other direction): a truncation that resolves is not a failure")

    # --- #208 EXPECTED OBSERVATION: the exit-code blindness, both directions ---
    obs_bad = _row("E-15", evidence="`ls knowledge`", rc=0,
                   expect_stdout_contains="_this_string_is_not_in_the_listing_9f3a")
    rows, _ = CT.load(write("obs1.jsonl", [obs_bad]))
    _, mism_o, _ = sample(rows, 5, 205)
    if not mism_o:
        fails.append("EXIT-CODE BLINDNESS: a command that exits 0 while its stdout CONTRADICTS "
                     "the row was passed — this is the #208 finding, unfixed")
    else:
        print("  ✅ observation arm: rc=0 with contradicting stdout is an OBSERVATION MISMATCH")
    rows, _ = CT.load(write("obs2.jsonl", [_row("E-16", evidence="`ls knowledge`", rc=0,
                                                expect_stdout_contains="_validate_evidence.py")]))
    _, mism_o2, _ = sample(rows, 5, 205)
    if mism_o2:
        fails.append("REMOVAL NOT GREEN: a TRUE expected observation was reported as a mismatch")
    else:
        print("  ✅ observation arm (other direction): a true expectation reproduces")
    rows, _ = CT.load(write("obs3.jsonl", [_row("E-17", rc=0, expect_count=99,
                            evidence="`grep -c def knowledge/_claimtable.py`")]))
    _, mism_o3, _ = sample(rows, 5, 205)
    if not mism_o3:
        fails.append("expect_count: a wrong declared count was not caught")
    else:
        print("  ✅ expect_count arm: a wrong count is caught (`grep -c` exits 0 regardless)")
    _ndef = subprocess.run(["bash", "-c", "grep -c def knowledge/_claimtable.py"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    rows, _ = CT.load(write("obs4.jsonl", [_row("E-18", rc=0, expect_count=int(_ndef),
                            evidence="`grep -c def knowledge/_claimtable.py`")]))
    _, mism_o4, _ = sample(rows, 5, 205)
    if mism_o4:
        fails.append("expect_count (other direction): the TRUE count was reported as a mismatch")
    else:
        print("  ✅ expect_count arm (other direction): the true count (%s) reproduces" % _ndef)
    # a declared observation is never left to the seeded draw
    many_o = [_row("D-%02d" % i, evidence="`ls knowledge` -> rc=0", rc=0) for i in range(30)]
    many_o.append(_row("Z-1", evidence="`ls knowledge` -> rc=0", rc=0,
                       expect_stdout_contains="_nope_9f3a"))
    rows, _ = CT.load(write("forced.jsonl", many_o))
    _, mism_f, _ = sample(rows, 1, 205)
    if not any(i == "Z-1" for i, _, _, _ in mism_f):
        fails.append("FORCED DRAW: a row carrying a declared observation was left to chance in a "
                     "31-row table sampled at n=1 — an expectation must always be checked")
    else:
        print("  ✅ forced-draw arm: a row with a declared observation is ALWAYS sampled")

    # --- direction 2: REMOVE the defects — the same rows go green ---
    rows, _ = CT.load(write("clean.jsonl", [_row("E-1"), _row("E-2",
                            evidence="`git ls-files knowledge/_claimtable.py` -> rc=0")]))
    if lint(rows):
        fails.append("REMOVAL NOT GREEN: repaired rows still fail: %r" % lint(rows))
    else:
        print("  ✅ removal green: repaired rows carry probeable tokens and lint clean")

    # --- SAMPLER: rc mismatch must be caught, then its removal green ---
    rows, _ = CT.load(write("mism.jsonl", [_row("E-4", evidence="`ls /no/such/dir/9f3a` -> rc=0",
                                                rc=0)]))
    _, mism, refus = sample(rows, 5, 205)
    if not mism:
        fails.append("PLANT NOT CAUGHT: a command whose real rc != declared rc was not flagged")
    else:
        print("  ✅ plant caught (rc mismatch): %s declared rc=%d, ran rc=%d"
              % (mism[0][0], mism[0][3], mism[0][2]))
    rows, _ = CT.load(write("ok.jsonl", [_row("E-5", evidence="`ls knowledge` -> rc=0", rc=0)]))
    _, mism2, _ = sample(rows, 5, 205)
    if mism2:
        fails.append("REMOVAL NOT GREEN: a correct rc was reported as a mismatch")
    else:
        print("  ✅ removal green: a correct declared rc reproduces")

    # --- REFUSAL arm: a side-effecting command must be REFUSED, not run ---
    rows, _ = CT.load(write("ref.jsonl", [_row("E-6",
                            evidence="`python3 knowledge/_validate_state_contrast.py` -> rc=0")]))
    _, _, refus = sample(rows, 5, 205)
    if not any(v == "SIDE-EFFECTS" for _, v, _, _ in refus):
        fails.append("REFUSAL ARM: a bare _validate_*.py was RUN or silently passed — it rewrites "
                     "a tracked audit; #204 declared this stop")
    else:
        print("  ✅ refusal arm: a bare `_validate_*.py` is REFUSED [SIDE-EFFECTS], not run")
    # #208: a marker inside a FILE NAME is a name, not an action — both directions.
    if classify("grep -c PREFIX_ACK knowledge/_git_commit.sh")[0] != "RUNNABLE":
        fails.append("PATH-NAME REFUSAL: a read-only grep was refused because its FILE NAME "
                     "contains an unsafe verb — every claim about that file is then unverifiable")
    else:
        print("  ✅ path-name arm: `grep … knowledge/_git_commit.sh` is RUNNABLE, not UNSAFE")
    for _c in ("git commit -m x", "git checkout HEAD~1", "git push origin master",
               "ls knowledge > /var/tmp/out"):
        if classify(_c)[0] != "UNSAFE":
            fails.append("UNSAFE TOO LOOSE: %r was not refused" % _c)
    print("  ✅ path-name arm (other direction): git commit/checkout/push and a redirect are "
          "still REFUSED [UNSAFE]")
    rows, _ = CT.load(write("unsafe.jsonl", [_row("E-7", evidence="`python3 -c \"print(1)\"` -> rc=0")]))
    _, _, refus2 = sample(rows, 5, 205)
    if not any(v == "UNSAFE" for _, v, _, _ in refus2):
        fails.append("REFUSAL ARM: `python3 -c` was not refused as UNSAFE")
    else:
        print("  ✅ refusal arm: `python3 -c` is REFUSED [UNSAFE], not defaulted to a pass")

    # --- DETERMINISM arm: the same seed draws the same rows ---
    many = [_row("D-%02d" % i, evidence="`ls knowledge` -> rc=0", rc=0) for i in range(20)]
    rows, _ = CT.load(write("many.jsonl", many))
    a = [r["id"] for r in random.Random(7).sample(rows, 4)]
    b = [r["id"] for r in random.Random(7).sample(rows, 4)]
    c = [r["id"] for r in random.Random(8).sample(rows, 4)]
    if a != b:
        fails.append("DETERMINISM: the same seed drew different rows (%r vs %r)" % (a, b))
    elif a == c:
        fails.append("DETERMINISM: two different seeds drew an identical sample — seeding is inert")
    else:
        print("  ✅ determinism arm: seed 7 draws %r twice; seed 8 draws %r" % (a, c))

    # --- #308 (s308-D29): judge at the commit, env → could-not-ask, absence, tool base, notes
    _selftest_308(fails)

    # --- #219 NO-MATERIAL arm: bare invocation, BOTH directions, driven not asserted ---------
    # The clause under test is the one that turned the first of the four s219-D5(Q5) packed-gate
    # reds green. It is proved by MOVING THE INPUT, never by an env var: ROOT is repointed at a
    # throwaway tree, so this reproduces on any machine [[gate-cannot-pass-in-one-environment]].
    # ⚠ BOTH cwd AND ROOT are moved. `main()` resolves a path against cwd FIRST and only then
    # against ROOT, so repointing ROOT alone left arm (c) silently linting the REAL notes/_claims
    # (360 dead pointers, exit 1 — a pass for the wrong reason). Caught by reading the output.
    _real_root, _real_cwd = ROOT, os.getcwd()
    _tmp = tempfile.mkdtemp(prefix="ev-nomat-")
    try:
        os.chdir(_tmp)
        # (a) no notes/_claims at all -> COULD-NOT-ASK (77), never 1 and never 0
        ROOT = _tmp
        rc = main([])
        if rc != CNA.EXIT:
            fails.append("NO-MATERIAL ARM: a bare run with no notes/_claims returned %r, want "
                         "%d (COULD-NOT-ASK). A gate with nothing to look at has found no defect, "
                         "and rc=2 is bad arguments, not a verdict." % (rc, CNA.EXIT))
        else:
            print("  ✅ no-material arm: bare + no notes/_claims -> COULD-NOT-ASK (%d), named"
                  % CNA.EXIT)
        # (b) the directory exists but is empty -> still a refusal, with its own reason
        os.makedirs(os.path.join(_tmp, "notes", "_claims"))
        if main([]) != CNA.EXIT:
            fails.append("NO-MATERIAL ARM: an EMPTY notes/_claims did not refuse")
        else:
            print("  ✅ no-material arm: an empty notes/_claims refuses too, with its own reason")
        # (c) ⛔ THE OTHER DIRECTION — the refusal must not swallow the gate. Plant a row that
        #     the linter is known to fail on; bare must now find it and exit 1, not refuse.
        with open(os.path.join(_tmp, "notes", "_claims", "planted.jsonl"), "w",
                  encoding="utf-8") as f:
            f.write(json.dumps(_row("NM-1", tag="PROVEN",
                                    evidence="no command, no path, no figure")) + "\n")
        rc = main(["--no-sample"])
        if rc != 1:
            fails.append("NO-MATERIAL ARM (other direction): a bare run over a PLANTED bad row "
                         "returned %r, want 1 — the default is defaulting to a pass" % rc)
        else:
            print("  ✅ no-material arm (other direction): bare over a planted bad row still "
                  "exits 1 — the refusal has not swallowed the gate")
    finally:
        os.chdir(_real_cwd)
        ROOT = _real_root
        shutil.rmtree(_tmp, ignore_errors=True)

    shutil.rmtree(tmp, ignore_errors=True)   # #308: the plant tree was never removed before
    if fails:
        print("⛔ _validate_evidence selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _validate_evidence selftest PASS — lint plants caught and cleared, sampler catches "
          "an rc mismatch, refusals are named not defaulted, seeding is reproducible; #308 rows are "
          "judged at their commit, environment is COULD-NOT-ASK, absence and tool-base paths "
          "read right, and only a DECLARED note excuses a token-less row.")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
