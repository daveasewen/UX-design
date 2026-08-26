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

USAGE
  python3 knowledge/_validate_evidence.py <rows.jsonl> [<rows2.jsonl> …]
                                          [--sample N] [--seed S] [--no-sample] [--strict-sample]
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

import sys, os, re, json, glob, random, shutil, subprocess
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
    out = []
    for m in PATH_RE.finditer(ev):
        p = m.group(1)
        nxt = ev[m.end():m.end() + 1]
        if nxt in GLOB_NEXT or p.endswith("-") or p.endswith("/"):
            continue
        if NONREPO_MARKER in ev[m.end():m.end() + NONREPO_WINDOW]:
            out.append((p, "NON-REPO"))
        elif ev[max(0, m.start() - len(ABSENT_PREFIX)):m.start()] == ABSENT_PREFIX:
            out.append((p, "ABSENT"))
        elif nxt == ELLIPSIS:
            out.append((p, "PREFIX"))
        else:
            out.append((p, "EXISTS"))
    return out


def paths_in(ev):
    """Repo-relative path POINTERS. A match followed by a glob metacharacter or an ellipsis is a
    PATTERN, not a pointer, and is excluded — `reviews/REVIEW-204-*.html` names a real family of
    files, and reporting it as a dead pointer is a false positive that would train a reader to
    ignore the check (found by driving this linter on the #204 tables, fix loop amendment ②)."""
    return [p for p, mode in pointers(ev) if mode == "EXISTS"]


def tokens(row):
    ev = row.get("evidence", "")
    cmds = commands(row)
    paths = pointers(ev)
    figs = FIGURE_RE.findall(ev)
    return cmds, paths, figs


def lint(rows):
    """[(id, reason)] — one entry per s182-D1 failure. Empty == conformant."""
    fails = []
    for r in rows:
        cmds, paths, figs = tokens(r)
        for p, mode in paths:
            p2 = p.rstrip(".,;:)")
            abs_p = os.path.join(ROOT, p2.split(":")[0])
            if mode == "NON-REPO":
                continue      # s191-D2: the home is DECLARED elsewhere; not this linter's to judge
            if mode == "ABSENT":
                if os.path.exists(abs_p):
                    fails.append((r["id"], "FALSE ABSENCE: evidence declares `absent:%s`, but that "
                                           "path EXISTS on disk — an absence claim whose subject is "
                                           "present is the same defect as a dead pointer, mirrored"
                                  % p2))
            elif mode == "PREFIX":
                # #208: a trailing ellipsis is a TRUNCATION, not a licence. Resolve it.
                if not glob.glob(abs_p + "*"):
                    fails.append((r["id"], "DEAD POINTER (truncated): evidence names `%s…`, and NO "
                                           "path on disk starts with it — the trailing ellipsis "
                                           "does not make a dead pointer legal (#208 laundering "
                                           "hole). Write the full path, or `absent:%s` if the "
                                           "ABSENCE is the claim, or add the ruled "
                                           "`(NON-REPO: <where>)` marker" % (p2, p2)))
            elif not os.path.exists(abs_p):
                fails.append((r["id"], "DEAD POINTER: evidence names `%s`, which does not exist "
                                       "on disk — a dead pointer reads as evidence. If the "
                                       "ABSENCE is the claim, write `absent:%s`; if the file "
                                       "lives outside the repo, use the ruled s191-D2 marker "
                                       "`(NON-REPO: <where>)`" % (p2, p2)))
        if not is_mechanical(r):
            continue
        if not (cmds or paths or figs):
            fails.append((r["id"], "s182-D1: MECHANICAL row (tag=%s verdict=%s) carries NO "
                                   "probeable token — no command, no existing path, no figure. "
                                   "Evidence: %r" % (r.get("tag"), r.get("verdict"),
                                                     r.get("evidence", "")[:90])))
    return fails


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


def sample(rows, n, seed, strict=False):
    """Seeded re-run of a subset. Returns (results, mismatches, refusals).

    #208: `mismatches` now carries BOTH kinds of divergence — an rc mismatch and an OBSERVATION
    mismatch — because both mean the same thing to a caller: the evidence no longer reproduces."""
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
    for r in drawn:
        cmd = commands(r)[0]
        verdict, reason = classify(cmd)
        if verdict != "RUNNABLE":
            refusals.append((r["id"], verdict, cmd, reason))
            print("  ⛔ REFUSED [%s] %s — `%s`\n      %s" % (verdict, r["id"], cmd[:100], reason))
            continue
        try:
            p = subprocess.run(["bash", "-c", cmd], cwd=ROOT, capture_output=True,
                               text=True, timeout=30, stdin=subprocess.DEVNULL)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            # An evidence command quoted without its file operand (`grep -c 'x'`) would read
            # stdin forever. stdin is closed above; a timeout now means the command genuinely
            # does not terminate, and that is a REFUSAL, never a pass.
            refusals.append((r["id"], "DOES-NOT-TERMINATE", cmd, "no exit within 30s"))
            print("  ⛔ REFUSED [DOES-NOT-TERMINATE] %s — `%s` did not exit within 30s"
                  % (r["id"], cmd[:80]))
            continue
        except Exception as e:
            refusals.append((r["id"], "NOT-IN-ENV", cmd, "execution raised %s" % e))
            print("  ⛔ REFUSED [NOT-IN-ENV] %s — `%s` raised %s" % (r["id"], cmd[:80], e))
            continue
        declared = r.get("rc")
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
    if refusals:
        print("── DECLARED GAP: %d of %d sampled row(s) were NOT run. Refusal is the honest "
              "answer; none of them is counted as a pass." % (len(refusals), len(drawn)))
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
        if not glob.glob(os.path.join(default, "*.jsonl")):
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
            found = sorted(glob.glob(os.path.join(cand, "*.jsonl")))
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

    rows, residual = [], 0
    for p in paths:
        rs, defects = CT.load(p)
        residual += CT.report_defects(defects, p)
        rows.extend(rs)
    print("evidence linter: %d row(s) from %d file(s) · %d mechanical"
          % (len(rows), len(paths), sum(1 for r in rows if is_mechanical(r))))

    fails = lint(rows)
    for i, reason in fails:
        print("  ⛔ %s — %s" % (i, reason))
    print("── s182-D1 LINT: %d failure(s)" % len(fails))

    mism, refus = [], []
    if "--no-sample" not in argv:
        _, mism, refus = sample(rows, n, seed, strict)

    bad = len(fails) + residual + len(mism) + (len(refus) if strict else 0)
    if bad:
        print("⛔ EVIDENCE GATE FAIL — %d lint · %d unparsed · %d rc/observation mismatch%s"
              % (len(fails), residual, len(mism),
                 " · %d refusal(s) under --strict-sample" % len(refus) if strict else ""))
        return 1
    nobs = sum(1 for r in rows if "expect_stdout_contains" in r or "expect_count" in r)
    print("✅ EVIDENCE GATE PASS — every mechanical row carries a probeable token; "
          "0 rc/observation mismatch(es); %d row(s) carried a declared OBSERVATION and every one "
          "reproduced; %d declared refusal(s)." % (nobs, len(refus)))
    if not nobs:
        print("⚠ NOT ONE ROW declared an expected observation (`expect_stdout_contains` / "
              "`expect_count`). For read-style evidence this run proved the commands still RUN, "
              "not that they still SAY what the rows claim (#208, the exit-code blindness).")
    return 0


# ---- selftest: plant-then-detect BOTH directions -----------------------------------------------

def _row(i, **kw):
    return dict({"id": i, "kind": "claim", "claim": "c", "evidence": "`ls knowledge` -> rc=0",
                 "tag": "PROVEN", "rc": 0}, **kw)


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

    if fails:
        print("⛔ _validate_evidence selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _validate_evidence selftest PASS — lint plants caught and cleared, sampler catches "
          "an rc mismatch, refusals are named not defaulted, seeding is reproducible.")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
