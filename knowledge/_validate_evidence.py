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

LEG 2 — SAMPLING. A seeded random subset of rows has its first COMMAND token RE-RUN and its
exit code compared with the row's declared `rc`. `--seed` makes every run reproducible; the
seed and the drawn ids are PRINTED, so a report can quote which rows were actually sampled.

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
      · 2 bad invocation.

CONSUMER at birth: the PM-wave seam, alongside `_join_claim_tables.py`. Declared: NOT wired
into `_build_all.py` or CI until item 1 is driven in >= 1 real wave (`s204-D1`).

Selftest: plants a token-less mechanical row, a dead path pointer, and an rc mismatch — each
must be named; removing each must go green. Includes a REFUSAL arm proving a side-effecting
command is refused rather than run, and a determinism arm proving the same seed draws the
same rows.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import sys, os, re, json, random, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _claimtable as CT

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


GLOB_NEXT = ("*", "?", "[", "\u2026")


def paths_in(ev):
    """Repo-relative path POINTERS. A match followed by a glob metacharacter or an ellipsis is a
    PATTERN, not a pointer, and is excluded — `reviews/REVIEW-204-*.html` names a real family of
    files, and reporting it as a dead pointer is a false positive that would train a reader to
    ignore the check (found by driving this linter on the #204 tables, fix loop amendment ②)."""
    out = []
    for m in PATH_RE.finditer(ev):
        nxt = ev[m.end():m.end() + 1]
        if nxt in GLOB_NEXT or m.group(1).endswith("-") or m.group(1).endswith("/"):
            continue
        out.append(m.group(1))
    return out


def tokens(row):
    ev = row.get("evidence", "")
    cmds = commands(row)
    paths = paths_in(ev)
    figs = FIGURE_RE.findall(ev)
    return cmds, paths, figs


def lint(rows):
    """[(id, reason)] — one entry per s182-D1 failure. Empty == conformant."""
    fails = []
    for r in rows:
        cmds, paths, figs = tokens(r)
        for p in paths:
            p2 = p.rstrip(".,;:)")
            if not os.path.exists(os.path.join(ROOT, p2.split(":")[0])):
                fails.append((r["id"], "DEAD POINTER: evidence names `%s`, which does not exist "
                                       "on disk — a dead pointer reads as evidence" % p2))
        if not is_mechanical(r):
            continue
        if not (cmds or paths or figs):
            fails.append((r["id"], "s182-D1: MECHANICAL row (tag=%s verdict=%s) carries NO "
                                   "probeable token — no command, no existing path, no figure. "
                                   "Evidence: %r" % (r.get("tag"), r.get("verdict"),
                                                     r.get("evidence", "")[:90])))
    return fails


def classify(cmd):
    """(verdict, reason). verdict ∈ RUNNABLE | SIDE-EFFECTS | UNSAFE | NOT-IN-ENV."""
    head = cmd.split()[0]
    for m in UNSAFE_MARKERS:
        if m in cmd:
            return "UNSAFE", "contains %r — arbitrary effect, no allowlist can vouch for it" % m
    if head in ("python3", "python"):
        if " -c" in cmd:
            return "UNSAFE", "`python3 -c` runs arbitrary code — cannot be judged read-only"
        if "--check" in cmd or "--selftest" in cmd or "--dry-run" in cmd:
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


def sample(rows, n, seed, strict=False):
    """Seeded re-run of a subset. Returns (results, mismatches, refusals)."""
    pool = [r for r in rows if commands(r)]
    rng = random.Random(seed)
    drawn = rng.sample(pool, min(n, len(pool))) if pool else []
    drawn.sort(key=lambda r: r["id"])
    results, mismatches, refusals = [], [], []
    print("── SAMPLER · seed=%d · pool=%d row(s) with a command · drawn=%d: %s"
          % (seed, len(pool), len(drawn), ", ".join(r["id"] for r in drawn) or "none"))
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
        if declared is None:
            print("  ⚠ RAN (no declared rc to compare) %s — `%s` → rc=%d" % (r["id"], cmd[:80], rc))
        elif rc != declared:
            mismatches.append((r["id"], cmd, rc, declared))
            print("  ⛔ RC MISMATCH %s — `%s` → rc=%d, row declares rc=%d"
                  % (r["id"], cmd[:80], rc, declared))
        else:
            print("  ✅ RAN %s — `%s` → rc=%d (matches declared)" % (r["id"], cmd[:80], rc))
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
        sys.stderr.write("✖ REFUSED: need at least one <rows.jsonl>\n")
        return 2
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
        print("⛔ EVIDENCE GATE FAIL — %d lint · %d unparsed · %d rc mismatch%s"
              % (len(fails), residual, len(mism),
                 " · %d refusal(s) under --strict-sample" % len(refus) if strict else ""))
        return 1
    print("✅ EVIDENCE GATE PASS — every mechanical row carries a probeable token; "
          "0 rc mismatch(es); %d declared refusal(s)." % len(refus))
    return 0


# ---- selftest: plant-then-detect BOTH directions -----------------------------------------------

def _row(i, **kw):
    return dict({"id": i, "kind": "claim", "claim": "c", "evidence": "`ls knowledge` -> rc=0",
                 "tag": "PROVEN", "rc": 0}, **kw)


def selftest():
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
